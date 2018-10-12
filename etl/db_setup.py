import sqlite3

def main():
    with sqlite3.connect('permitplans.db') as conn:

        c = conn.cursor()

        # Create plans table
        c.execute('''CREATE TABLE plan (
                     id INTEGER PRIMARY KEY,
                     package TEXT, 
                     location TEXT, 
                     sheetno INTEGER)''')

        # Create permits table
        c.execute('''CREATE TABLE permit (
                     id INTEGER PRIMARY KEY,
                     address TEXT, 
                     apno INTEGER, 
                     aptype TEXT, 
                     examiner TEXT, 
                     apdttm TEXT)''')

        # Create plan_permit table to allow for many-to-many relationship
        c.execute('''CREATE TABLE plan_permit (
                     id INTEGER PRIMARY KEY,
                     plan_id INTEGER,
                     permit_id INTEGER)''')

        conn.commit()

if __name__ == '__main__':
    main()