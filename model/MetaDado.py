from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from lib.Db import db_base

class MetaDado(db_base):
    __tablename__ = "meta_dado"

    id = Column(Integer, primary_key=True)
    chave = Column("chave", String)
    valor = Column("valor", String)
    base_historica_id = Column(Integer, ForeignKey("base_historica.id"))
    base_historica = relationship("BaseHistorica", back_populates="dados")