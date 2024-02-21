# coding: utf-8
from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

import uvicorn
from fastapi.staticfiles import StaticFiles
#引用路由
from frp import api as frp_api
from app.game.Palworld import Api as PalworldApi

app = FastAPI(docs_url=None)
security = HTTPBasic()

app.include_router(frp_api.router)
app.include_router(PalworldApi.router)

doc_user_name = 'admin'
doc_password = 'jc123456'
# 文档
@app.get("/docs",include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != doc_user_name or credentials.password != doc_password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    
# @app.get("/openapi.json",include_in_schema=False)
# async def get_documentation(credentials: HTTPBasicCredentials = Depends(security)):
#     if credentials.username != doc_user_name or credentials.password != doc_password:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     else:
#         return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
#默认访问内容

think_version = '6.1.4'
@app.get(path='/')
async def root():
    return HTMLResponse(content='<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"> <h1>:) </h1><p> ThinkPHP V' + think_version + '<br/><span style="font-size:30px;">16载初心不改 - 你值得信赖的PHP框架</span></p><span style="font-size:25px;">[ V6.0 版本由 <a href="https://www.yisu.com/" target="yisu">亿速云</a> 独家赞助发布 ]</span></div><script type="text/javascript" src="https://e.topthink.com/Public/static/client.js"></script><think id="ee9b1aa918103c4fc"></think>')

#静态资源
app.mount('/', StaticFiles(directory="public"), 'public')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)