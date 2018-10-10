import sqlite3

from li_dbs import GISLNI
from sql_queries import truncate_query, permit_to_cloud_query


def truncate(query, con):
    print('Truncating the target table...')
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()
    con.commit()
    print('Table successfully truncated.')

def etl(query, source_con, target_con):
    # extract data from source
    print('Extracting the data from the source database...')
    source_cursor = source_con.cursor()
    source_cursor.execute(query.extract_query)
    data = source_cursor.fetchall()
    source_cursor.close()

    # load data into target
    if data:
        print(f'Loading {len(data)} rows into the target database...')
        target_cursor = target_con.cursor()
        target_cursor.executemany(query.load_query, data)
        target_cursor.close()
        target_con.commit()
        print('ETL process complete.')
    else:
        print('No data to ETL')

def truncate_and_etl():
    with GISLNI.GISLNI() as source, sqlite3.connect('permitplans.db') as target:
        truncate(truncate_query, target)
        etl(permit_to_cloud_query, source, target)

if __name__ == '__main__':
    truncate_and_etl()