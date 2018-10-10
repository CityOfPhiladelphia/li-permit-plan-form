from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import USERNAME, PASSWORD, HOSTNAME, PORT, SERVICE_NAME
import os
import csv
from flask import g


def get_db():
    if 'db' not in g:
        import cx_Oracle
        oracle_connection_string = (
            'oracle+cx_oracle://{username}:{password}@' +
            cx_Oracle.makedsn('{hostname}', '{port}', '{service_name}')
        )
        engine = create_engine(
                    oracle_connection_string.format(
                        username=USERNAME,
                        password=PASSWORD,
                        hostname=HOSTNAME,
                        port=PORT,
                        service_name=SERVICE_NAME
                    )
                )
        g.db = scoped_session(sessionmaker(bind=engine))
        g.db.engine = engine
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()