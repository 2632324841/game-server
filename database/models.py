from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float, DateTime, DECIMAL, Index
from sqlalchemy.orm import relationship
import math
from .database import Base


windows_steamcmd = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'



class Earthquake(Base):
    __tablename__ = "earthquake"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    zhenji = Column(Float(12,2))
    dizhen_time = Column(DateTime)
    latitude = Column(Float(13,8))
    longitude = Column(Float(13,8))
    depth = Column(DECIMAL(12,2))
    location = Column(String(256))
    Index('dizhen_time', 'dizhen_time'),
    
class UserStatistics(Base):
    __tablename__ = 'xm_user_statistics'
    id = Column(Integer, primary_key=True,autoincrement=True)  # 主键 autoincrement=True 自增
    log_id = Column(Integer)  # 主键 autoincrement=True 自增
    callbackcount = Column(String(256))
    daohuodi = Column(String(256))
    realScode = Column(String(128))
    wechatNumber = Column(String(64))

    provinceName = Column(String(64))
    cityName = Column(String(64))
    countyName = Column(String(64))
    pdtName = Column(String(128))
    mobile = Column(String(11))

    entId = Column(Integer)
    longitude = Column(String(32))
    latitude = Column(String(32))
    code = Column(String(128))
    scode = Column(String(128))
    outCode = Column(String(128))
    addTime = Column(String(16))

    Index('realScode', 'realScode'),
    Index('code', 'code'),
    
class FrpRelease(Base):
    __tablename__ = "frp_release"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    tag = Column(String(64))
    releas = Column(String(64))
    text = Column(Text)
    version = Column(Integer)
    release_time = Column(DateTime)
    
    Index('tag', 'tag'),
    
    def pagination(session, page = 1, pageSize = 10):
        count = session.count()
        last_page = math.ceil(count / pageSize)
        data_list = session.offset((page-1)*pageSize).limit(pageSize).all()
        data = {
            'page':page,
            'count':count,
            'data':data_list,
            'page_size':pageSize,
            'last_page':last_page,
        }
        return data

class FrpAssets(Base):
    __tablename__ = "frp_assets"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    tag = Column(String(64))
    filename = Column(String(256))
    software = Column(String(256))
    edition = Column(String(256))
    system = Column(String(256))
    machine = Column(String(256))
    format = Column(String(256))
    url = Column(String(2048))
    filesize = Column(String(256))
    release_time = Column(DateTime)
    
    Index('tag', 'tag'),
    releas_id = Column(Integer, ForeignKey("frp_release.id", ondelete="CASCADE"))
    
    def pagination(session, page = 1, pageSize = 10):
        count = session.count()
        last_page = math.ceil(count / pageSize)
        data_list = session.offset((page-1)*pageSize).limit(pageSize).all()
        data = {
            'page':page,
            'count':count,
            'data':data_list,
            'page_size':pageSize,
            'last_page':last_page,
        }
        return data
    
class AppIssueRecord(Base):
    __tablename__ = "app_issue_record"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    # 应用名称
    app_name = Column(String(192))
    # 开发者
    developer = Column(String(256))
    # 来源
    source = Column(String(256))
    # 版本号
    version = Column(String(256))
    # 问题
    problem = Column(String(2048))
    # 文件
    file = Column(String(256))
    # 发布时间
    release_time = Column(DateTime)
    
    Index('app_name', 'app_name'),
    
    def pagination(session, page = 1, pageSize = 10):
        count = session.count()
        last_page = math.ceil(count / pageSize)
        data_list = session.offset((page-1)*pageSize).limit(pageSize).all()
        data = {
            'page':page,
            'count':count,
            'data':data_list,
            'page_size':pageSize,
            'last_page':last_page,
        }
        return data
    
class AppSdkRecord(Base):
    __tablename__ = "app_sdk_record"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    # sdk名称
    sdk_name = Column(String(192))
    # 开发者
    developer = Column(String(256))
    # 来源
    source = Column(String(256))
    # 版本
    version = Column(String(256))
    # 问题
    problem = Column(String(2048))
    # 文件
    file = Column(String(256))
    # 发布时间
    release_time = Column(DateTime)
    
    Index('sdk_name', 'sdk_name'),
    
    def pagination(session, page = 1, pageSize = 10):
        count = session.count()
        last_page = math.ceil(count / pageSize)
        data_list = session.offset((page-1)*pageSize).limit(pageSize).all()
        data = {
            'page':page,
            'count':count,
            'data':data_list,
            'page_size':pageSize,
            'last_page':last_page,
        }
        return data