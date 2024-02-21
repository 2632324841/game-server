# coding: utf-8
from fastapi import APIRouter
# from sqlalchemy.orm import Session
import zipfile
from sqlalchemy.orm import sessionmaker
from database import crud, models, schemas
from database.database import SessionLocal, engine, Session
from datetime import datetime, timedelta
from database.models import FrpRelease, FrpAssets
from frp.frp import Frp
import math
from threading import Thread
import platform,os
from common.responseModel import response
import requests
from common.cache import create_cache

# 获取操作系统名称
os_name = platform.system()
steamcmd_path = os.path.join(os.getcwd(), 'steamcmd')
if os.path.isdir(steamcmd_path) == False:
    os.mkdir(steamcmd_path)
windows = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'

router = APIRouter(prefix='/install', tags=['install'])
cache = create_cache('file')

@router.get('/query_system_is_support')
async def query_system_is_support():
    if os_name == "Windows":
        return response(data=True)
    else:
        return response(message='当前系统暂不支持，开发人员正在火速开发中！',data=False)

@router.get('/query_is_install')
async def query_is_install():
    file = os.path.join(os.getcwd(), 'install.lock')
    if os.path.isfile(file):
        return response(data=True)
    else:
        return response(message='已经安装成功了',data=False, success=False)
    
@router.get('/install_steamcmd')
async def install_steamcmd():
    if cache.exists('install_steamcmd') == True:
        return response(message='已经在下载了', success=False)
    t = Thread(target=install_steamcmd_task, args=())  # 创建线程
    t.name = 'update_frp'
    t.start()  # 启动线程
    return response(message='开始安装')

@router.get('/install_steamcmd_progress')
async def install_steamcmd_progress():
    if cache.exists('install_steamcmd') == False:
        return response(message='还没有开始安装', success=False)
    return response(data=cache.get('install_steamcmd'))

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
def install_steamcmd_task():
    windows_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
    download_path = os.path.join(steamcmd_path, 'steamcmd.zip')

    with requests.get(windows_url, stream=True) as r, open(download_path, 'wb') as f:
        total_size = int(r.headers.get('content-length', 0))
        downloaded_size = 0

        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
            downloaded_size += len(chunk)

            # 计算下载进度百分比
            progress_percentage = (downloaded_size / total_size) * 100
            if progress_percentage == 100:
                unzip_file(download_path, steamcmd_path)
            cache.set('install_steamcmd', {'progress':progress_percentage, 'text':"已下载: "+str(downloaded_size)+" 字节, 总大小: "+str(total_size)+" 字节, 进度: "+str(round(progress_percentage, 2))+"%"})
            
def setamcmd_init():
    pass

