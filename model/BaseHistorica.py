from bs4 import BeautifulSoup

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.Db import db_base

class BaseHistorica(db_base):
    __tablename__ = "base_historica"

    id = Column(Integer, primary_key=True)
    dados = relationship("MetaDado", back_populates="base_historica")