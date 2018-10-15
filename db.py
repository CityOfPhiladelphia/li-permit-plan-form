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
              WHERE permit.apno = {apno}"""
    permit = db.engine.execute(text(sql)).fetchone()
    return permit

def get_plans(apno):
    db = get_db()
    sql = f"""SELECT * FROM plan
              INNER JOIN plan_permit ON plan.id = plan_permit.plan_id
              INNER JOIN permit ON permit.id = plan_permit.permit_id
              WHERE permit.apno = {apno}"""
    plans = db.engine.execute(text(sql)).fetchall()
    return plans

# def get_apnos_from_plan(plan_id, apno):
#     db = get_db()
#     sql = f"""SELECT apno FROM permit
#               INNER JOIN plan_permit ON permit.id = plan_permit.id
#               INNER JOIN plan ON plan.id = plan_permit.id
#               WHERE plan.id = {plan_id}
#               AND apno != {apno}"""
#     apnos = db.engine.execute(text(sql)).fetchall()
#     return apnos

def get_permit_address(apno):
    # Ensure apno is an integer
    try:
        int(apno)
    except ValueError:
        return False
    db = get_db()
    sql = f"""SELECT address FROM permit 
              WHERE apno = {apno}"""
    permit_address = db.engine.execute(text(sql)).fetchone()
    if permit_address is not None:
        permit_address = permit_address[0]
    return permit_address

def insert_plan(package, location, sheetno):
    db = get_db()

    # Insert the plan into the plan table
    plan_insert_sql = f"""INSERT INTO plan (package, location, sheetno)
                          VALUES ('{package}', '{location}', {sheetno})"""
    db.engine.execute(text(plan_insert_sql))

def insert_plan_permit(apno):
    db = get_db()
    
    # Get the latest plan_id
    plan_id_sql = """SELECT id
                     FROM plan
                     ORDER BY id DESC
                     LIMIT 1"""
    plan_id = db.engine.execute(text(plan_id_sql)).fetchone()[0]

    # Get the permit_id for the apno
    permit_id_sql = f"""SELECT id
                        FROM permit
                        WHERE apno = {apno}"""
    permit_id = db.engine.execute(text(permit_id_sql)).fetchone()[0]

    # Insert the plan_id and permit_id into the plan_permit table
    plan_permit_insert_sql = f"""INSERT INTO plan_permit (plan_id, permit_id)
                                 VALUES ({plan_id}, {permit_id})"""
    db.engine.execute(text(plan_permit_insert_sql))