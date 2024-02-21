from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
app = FastAPI()

# 存储 WebSocket 连接的字典
websockets_dict = {}
#静态资源
app.mount('/', StaticFiles(directory="public"), 'public')

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    # 存储 WebSocket 连接
    websockets_dict[client_id] = websocket

    while True:
        try:
            # 从 WebSocket 接收消息（命令）
            data = await websocket.receive_text()
            # 执行命令
            result = execute_command(data)
            # 发送命令执行结果到 WebSocket
            await websocket.send_text(result)
        except Exception as e:
            print(f"Error: {e}")
            break

    # 移除 WebSocket 连接
    del websockets_dict[client_id]


def execute_command(command: str) -> str:
    import subprocess
    try:
        # 执行命令并获取输出
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing command: {e}"


if __name__ == "__main__":
    import uvicorn

    # 启动 FastAPI 应用
    uvicorn.run(app, host="0.0.0.0", port=8000)
