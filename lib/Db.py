import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_FILE = "atas-constituinte.db"
con = None
db_base = declarative_base()
db_engine = create_engine('sqlite:///' + DB_FILE)
db_session = sessionmaker(bind=db_engine)

class Db:
    @staticmethod
    def start():
        if not Db.isInit():
            con = sqlite3.connect(DB_FILE)

    @staticmethod
    def isInit():
        return con != None

    @staticmethod
    def finish():
        if Db.isInit():
            con.close()
            con = None