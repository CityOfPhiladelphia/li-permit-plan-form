import cx_Oracle

from flask import g
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from config import USERNAME, PASSWORD, HOSTNAME, PORT, SERVICE_NAME


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

def get_permit(apno):
    db = get_db()
    sql = f"""SELECT * FROM plan_app_permit
              WHERE apno LIKE {apno}"""
    permit = db.engine.execute(text(sql)).fetchone()
    return permit

def get_plans(apno):
    db = get_db()
    sql = f"""SELECT * FROM plan_app_plan
              INNER JOIN plan_app_plan_permit ON plan_app_plan.id = plan_app_plan_permit.plan_id
              INNER JOIN plan_app_permit ON plan_app_permit.id = plan_app_plan_permit.permit_id
              WHERE plan_app_permit.apno LIKE {apno}"""
    plans = db.engine.execute(text(sql)).fetchall()
    return plans

def get_apnos_associated_with_plan(plan_id, apno):
    db = get_db()
    sql = f"""SELECT apno
              FROM plan_app_permit
              WHERE id IN 
              (
                  SELECT permit_id
                  FROM plan_app_plan_permit
                  WHERE plan_id = {plan_id}
              )
              AND plan_app_permit.apno NOT LIKE {apno}"""
    apnos = db.engine.execute(text(sql)).fetchall()
    return apnos

def get_permit_address(apno):
    # Ensure apno is an integer
    try:
        int(apno)
    except ValueError:
        return False
    db = get_db()
    sql = f"""SELECT address FROM plan_app_permit 
              WHERE apno LIKE '{apno}'"""
    permit_address = db.engine.execute(text(sql)).fetchone()
    if permit_address is not None:
        permit_address = permit_address[0]
    return permit_address

def insert_plan(package, location, sheetno):
    db = get_db()

    # Insert the plan into the plan table
    plan_insert_sql = f"""INSERT INTO plan_app_plan (package, location, sheetno)
                          VALUES ('{package}', '{location}', {sheetno})"""
    db.engine.execute(text(plan_insert_sql))

def insert_plan_permit(apno):
    db = get_db()
    
    # Get the latest plan_id
    plan_id_sql = """SELECT id
                     FROM plan_app_plan
                     ORDER BY id DESC"""
    plan_id = db.engine.execute(text(plan_id_sql)).fetchone()[0]

    # Get the permit_id for the apno
    permit_id_sql = f"""SELECT id
                        FROM plan_app_permit
                        WHERE apno LIKE {apno}"""
    permit_id = db.engine.execute(text(permit_id_sql)).fetchone()[0]

    # Insert the plan_id and permit_id into the plan_permit table
    plan_permit_insert_sql = f"""INSERT INTO plan_app_plan_permit (plan_id, permit_id)
                                 VALUES ({plan_id}, {permit_id})"""
    db.engine.execute(text(plan_permit_insert_sql))