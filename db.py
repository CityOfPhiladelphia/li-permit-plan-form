from flask import g
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


def get_db():
    if 'db' not in g:
        engine = create_engine('sqlite:///permitplans.db')
        g.db = scoped_session(sessionmaker(bind=engine))
        g.db.engine = engine
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_permit(apno):
    db = get_db()
    sql = f"""SELECT * FROM permit 
              LEFT JOIN plan_permit ON permit.id = plan_permit.permit_id
              LEFT JOIN plan ON plan.id = plan_permit.plan_id
              WHERE permit.apno = {apno}"""
    permit = db.engine.execute(text(sql)).fetchone()
    return permit