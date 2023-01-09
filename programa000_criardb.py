from lib.Db import db_base, db_engine

from model.BaseHistorica import BaseHistorica
from model.MetaDado import MetaDado

if __name__ == "__main__":
    db_base.metadata.drop_all(db_engine)
    db_base.metadata.create_all(db_engine)