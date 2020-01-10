from li_dbs import GISLNIDB


def main():
    with GISLNIDB.GISLNIDB() as conn:

        c = conn.cursor()

        # Create plans table
        c.execute('''CREATE TABLE plan_app_plan (
                        id NUMBER(20) PRIMARY KEY,
                        package VARCHAR2(254 BYTE), 
                        location VARCHAR2(254 BYTE),
                        comments VARCHAR(2000 BYTE),
                        dateadded TIMESTAMP(6),
                        editdate TIMESTAMP(6)
                     )''')

        # Create permits table
        c.execute('''CREATE TABLE plan_app_permit(
                        id NUMBER(20) PRIMARY KEY,
                        address VARCHAR2(254 BYTE), 
                        apno VARCHAR2(20 BYTE), 
                        aptype VARCHAR2(254 BYTE), 
                        examiner VARCHAR2(254 BYTE),
                        nopages NUMBER(10), 
                        apdttm DATE
                     )''')

        # Create plan_permit table to allow for many-to-many relationship
        c.execute('''CREATE TABLE plan_app_plan_permit (
                        id NUMBER(20) PRIMARY KEY,
                        plan_id NUMBER(20),
                        apno NUMBER(20)
                     )''')

        conn.commit()

if __name__ == '__main__':
    main()