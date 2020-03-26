from datetime import datetime

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
    named_params = {'apno': apno}
    sql = f"""SELECT * FROM plan_app_permit_test
              WHERE apno LIKE :apno"""
    permit = db.engine.execute(text(sql), named_params).fetchone()
    return permit

def get_plans(apno):
    db = get_db()
    named_params = {'apno': apno}
    sql = f"""SELECT * FROM plan_app_plan_test
              INNER JOIN plan_app_plan_permit_test ON plan_app_plan_test.id = plan_app_plan_permit_test.plan_id
              INNER JOIN plan_app_permit_test ON plan_app_permit_test.apno = plan_app_plan_permit_test.apno
              WHERE plan_app_permit_test.apno LIKE :apno"""
    plans = db.engine.execute(text(sql), named_params).fetchall()
    return plans

def get_apnos_associated_with_plan(plan_id, apno):
    db = get_db()
    named_params = {'apno': apno, 'plan_id': plan_id}
    sql = f"""SELECT apno
              FROM plan_app_permit_test
              WHERE apno IN 
              (
                  SELECT apno
                  FROM plan_app_plan_permit_test
                  WHERE plan_id = :plan_id
              )
              AND plan_app_permit_test.apno NOT LIKE :apno"""
    apnos = db.engine.execute(text(sql), named_params).fetchall()
    return apnos

def get_all_apnos_associated_with_plan(plan_id):
    db = get_db()
    named_params = {'plan_id': plan_id}
    sql = f"""SELECT apno
              FROM plan_app_plan_permit_test
              WHERE plan_id = :plan_id"""
    apnos = db.engine.execute(text(sql), named_params).fetchall()
    return apnos

def get_permit_address(apno):
    # Ensure apno is a string
    try:
        str(apno)
    except ValueError:
        return False
    db = get_db()
    named_params = {'apno': apno}
    sql = f"""SELECT address FROM plan_app_permit_test
              WHERE apno LIKE :apno"""
    permit_address = db.engine.execute(text(sql), named_params).fetchone()
    if permit_address is not None:
        permit_address = permit_address[0]
    return permit_address

def insert_plan(package, location, comments):
    db = get_db()
    named_params = {'package': package, 'location': location, 'comments': comments}

    # Insert the plan into the plan table
    plan_insert_sql = f"""INSERT INTO plan_app_plan_test (
                            package, 
                            location, 
                            comments, 
                            dateadded
                          )
                          VALUES (
                              :package,
                              :location,
                              :comments,
                              to_date('{datetime.now().date()}', 'yyyy-mm-dd')
                           )"""
    db.engine.execute(text(plan_insert_sql), named_params)

def insert_plan_permit(apno):
    db = get_db()
    
    # Get the latest plan_id
    plan_id_sql = """SELECT 
                        id
                     FROM 
                        plan_app_plan_test
                     ORDER BY 
                        id DESC"""
    plan_id = db.engine.execute(text(plan_id_sql)).fetchone()[0]

    named_params = {'plan_id': plan_id, 'apno': apno}

    # Insert the plan_id and apno into the plan_permit table
    plan_permit_insert_sql = f"""INSERT INTO plan_app_plan_permit_test (
                                    plan_id, 
                                    apno
                                 )
                                 VALUES (
                                     :plan_id,
                                     :apno
                                 )"""
    db.engine.execute(text(plan_permit_insert_sql), named_params)

def get_all_plans():
    db = get_db()

    all_plans_sql = """SELECT 
                           * 
                       FROM 
                           plan_app_plan_test
                       ORDER BY 
                           id"""

    plans = db.engine.execute(text(all_plans_sql)).fetchall()
    return plans

def get_plan_from_id(plan_id):
    db = get_db()
    named_params = {'plan_id': plan_id}

    plan_sql = f"""SELECT 
                       *
                   FROM 
                       plan_app_plan_test
                   WHERE 
                       id = :plan_id"""

    plan = db.engine.execute(text(plan_sql), named_params).fetchone()
    return plan

def delete_plan(plan_id):
    db = get_db()
    named_params = {'plan_id': plan_id}

    # Delete the plan from the plan table
    delete_plan_sql = f"""DELETE FROM plan_app_plan_test
                          WHERE id = :plan_id"""
    db.engine.execute(text(delete_plan_sql), named_params)

    # Delete the plan_permit entries for this plan
    delete_plan_permit_sql = f"""DELETE FROM plan_app_plan_permit_test
                                 WHERE plan_id = :plan_id"""
    db.engine.execute(text(delete_plan_permit_sql), named_params)

def update_plan(plan_id, package, location, comments):
    db = get_db()
    named_params = {'package': package, 'location': location, 'comments': comments, 'plan_id': plan_id}

    # Insert the plan into the plan table
    plan_insert_sql = f"""UPDATE plan_app_plan_test
                            SET package=:package,
                                location=:location,
                                comments=:comments,
                                editdate=to_date('{datetime.now().date()}', 'yyyy-mm-dd')
                            WHERE id = :plan_id"""
    db.engine.execute(text(plan_insert_sql), named_params)

def update_plan_permits(plan_id, apnos):
    db = get_db()
    named_params = {'plan_id': plan_id}

    # Delete the old plan_permits
    plan_permit_delete_sql = f"""DELETE FROM plan_app_plan_permit_test
                                   WHERE plan_id=:plan_id"""

    db.engine.execute(text(plan_permit_delete_sql), named_params)

    # Insert the new plan_permits
    for apno in apnos:
        named_params = {'plan_id': plan_id, 'apno': apno}

        plan_permit_insert_sql = f"""INSERT INTO plan_app_plan_permit_test (plan_id, apno)
                                    VALUES (:plan_id, :apno)"""

        # Add the new plan_permits
        db.engine.execute(text(plan_permit_insert_sql), named_params)