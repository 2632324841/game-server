from sqlalchemy.orm import Session
import datetime
from . import models, schemas

def query_earthquake(db: Session, dizhen_time: datetime, location : str):
    return db.query(models.Earthquake).filter(models.Earthquake.dizhen_time == dizhen_time,models.Earthquake.location == location).first()