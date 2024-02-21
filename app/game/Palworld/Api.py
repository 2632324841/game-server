# coding: utf-8
from fastapi import APIRouter
# from sqlalchemy.orm import Session

from sqlalchemy.orm import sessionmaker
from database import crud, models, schemas
from database.database import SessionLocal, engine, Session
from datetime import datetime, timedelta
import os
from database.models import FrpRelease, FrpAssets
from frp.frp import Frp
import math
from threading import Thread
from app.game.Palworld.Config import Config,NestedConfigParser
from common.responseModel import response
from app.game.Palworld.ApiModel import PalGameWorldSettings

router = APIRouter(prefix='/game/palworld', tags=['game'])

@router.get('/query_server_config')
async def query_server_config():
    text = Config().getPalWorldSettings()
    ConfigParser = NestedConfigParser()
    if text != '':
        print(text)
        ConfigParser.read_str(text)
        data = ConfigParser.get_nested('/Script/Pal.PalGameWorldSettings', 'OptionSettings')
    else:
        data = None
    return response(200, data=data)

@router.post('/set_server_config')
async def query_server_config(data: PalGameWorldSettings):
    text = Config().getPalWorldSettings()
    ConfigParser = NestedConfigParser()
    if text != '':
        print(text)
        ConfigParser.read_str(text)
        ConfigParser.set_nested('/Script/Pal.PalGameWorldSettings', 'OptionSettings', vars(data))
        path = Config().getPalWorldSettingsPath()
        ConfigParser.save(path)
    else:
        data = None
    return response(200, data=data)