# coding: utf-8
from fastapi import APIRouter
# from sqlalchemy.orm import Session

from sqlalchemy.orm import sessionmaker
from database import crud, models, schemas
from database.database import SessionLocal, engine, Session
from datetime import datetime, timedelta
import re
import time
import random
from database.models import FrpRelease, FrpAssets
from frp.frp import Frp
import math
from threading import Thread

router = APIRouter(prefix='/frp', tags=['frp'])

@router.get('/update_frp')
async def update_frp():
    frpObj = Frp()
    t = Thread(target=frpObj.update_frp, args=())  # 创建线程
    t.name = 'update_frp'
    t.start()  # 启动线程
    return {'code': 200, 'msg': '创建执行成功', 'data': []}


@router.get('/query_frp_edition')
async def query_frp_edition(page: int = 1):
    pageSize = 10
    session = sessionmaker(engine)()
    FrpReleaseData = session.query(FrpRelease).order_by(
        FrpRelease.version.desc()).offset((page-1)*pageSize).limit(pageSize).all()
    # count = session.query(FrpRelease).count()
    # last_page = math.ceil(count / pageSize)
    # FrpReleaseData = session.query(FrpRelease).order_by(FrpRelease.version.desc()).offset((page-1)*pageSize).limit(pageSize).all()
    # data = {
    #     'page':page,
    #     'count':count,
    #     'data':FrpReleaseData,
    #     'page_size':pageSize,
    #     'last_page':last_page,
    # }
    # s = session.query(FrpRelease).order_by(FrpRelease.version.desc())
    # FrpReleaseData = FrpRelease.pagination(s, 1)
    return {'code': 200, 'msg': '查询成功', 'data': FrpReleaseData}


@router.get('/query_frp_release')
async def query_frp_release(tag: str, page: int = 1):
    pageSize = 50
    session = sessionmaker(engine)()
    FrpAssetsList = session.query(FrpAssets).filter(FrpAssets.tag == tag).all()
    # FrpAssetsList = session.query(FrpAssets).filter(
    #     FrpAssets.tag == tag).offset((page-1)*pageSize).limit(pageSize).all()
    # count = session.query(FrpAssets).count()
    # last_page = math.ceil(count / pageSize)
    # FrpReleaseData = session.query(FrpAssets).order_by(FrpAssets.version.desc()).offset((page-1)*pageSize).limit(pageSize).all()
    # data = {
    #     'page':page,
    #     'count':count,
    #     'data':FrpReleaseData,
    #     'page_size':pageSize,
    #     'last_page':last_page,
    # }
    return {'code': 200, 'msg': '查询成功', 'data': FrpAssetsList}
