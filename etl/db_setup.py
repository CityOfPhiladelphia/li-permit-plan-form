import sqlite3

from li_dbs import GISLICLD


def main():
    with GISLICLD.GISLICLD() as conn:

        c = conn.cursor()

        # Create plans table
        c.execute('''CREATE TABLE plan_app_plan (
                     id NUMBER(20) PRIMARY KEY,
                     package VARCHAR2(254 BYTE), 
                     location VARCHAR2(254 BYTE), 
                     sheetno NUMBER(10),
                     comments VARCHAR(2000 BYTE),
                     dateadded TIMESTAMP(6))''')

        # Create permits table
        c.execute('''CREATE TABLE plan_app_permit (
                     id NUMBER(20) PRIMARY KEY,
                     address VARCHAR2(254 BYTE), 
                     apno VARCHAR2(20 BYTE), 
                     aptype VARCHAR2(254 BYTE), 
                     examiner VARCHAR2(254 BYTE), 
                     apdttm DATE,
                     
                     CONSTRAINT unique_permit UNIQUE (apno)
                     )''')

        # Create plan_permit table to allow for many-to-many relationship
        c.execute('''CREATE TABLE plan_app_plan_permit (
                     id NUMBER(20) PRIMARY KEY,
                     plan_id NUMBER(20),
                     permit_id NUMBER(20))''')

        conn.commit()

if __name__ == '__main__':
    main()