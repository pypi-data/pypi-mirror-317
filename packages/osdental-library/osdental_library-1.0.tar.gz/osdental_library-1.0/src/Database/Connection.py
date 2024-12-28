import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, PoolProxiedConnection
from sqlalchemy.orm import sessionmaker, Session
from Helpers.Message import DB_ENV_ERROR, DB_CONNECTION_ERROR

load_dotenv()

class DBConnection:
    
    def __init__(self):
        self.connection_string = os.getenv('DATABASE')
        if not self.connection_string:
            raise ValueError(DB_ENV_ERROR)
        
        self.engine = create_engine(self.connection_string)
        if self.engine is None:
            raise ValueError(DB_CONNECTION_ERROR)
        
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.session()
    
    def get_raw_conn(self) -> PoolProxiedConnection:
        return self.engine.raw_connection()