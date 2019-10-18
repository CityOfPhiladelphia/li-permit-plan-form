from li_dbs import GISLNI, GISLICLD
from sql_queries import truncate_query, permit_to_cloud_query

def get_logger():
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = logging.FileHandler('log.txt')
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def truncate(query, con, logger):
    logger.info('Truncating the target table...')
    print('Truncating the target table...')
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()
    con.commit()
    logger.info('Table successfully truncated.)
    print('Table successfully truncated.')


def etl(query, source_con, target_con, logger):
    # extract data from source
    logger.info('Extracting the data from the source database...')
    print('Extracting the data from the source database...')
    source_cursor = source_con.cursor()
    source_cursor.execute(query.extract_query)
    data = source_cursor.fetchall()
    source_cursor.close()

    # load data into target
    if data:
        logger.info(f'Loading {len(data)} rows into the target database...')
        print(f'Loading {len(data)} rows into the target database...')
        target_cursor = target_con.cursor()
        target_cursor.executemany(query.load_query, data)
        target_cursor.close()
        target_con.commit()
        logger.info('ETL process complete.')
        print('ETL process complete.')
    else:
        logger.info('No data to ETL')
        print('No data to ETL')

def truncate_and_etl():
    logger = get_logger()
    logger.info('---------------------------------')
    logger.info('ETL process initialized')
    with GISLNI.GISLNI() as source, GISLICLD.GISLICLD() as target:
        truncate(truncate_query, target, logger)
        etl(permit_to_cloud_query, source, target, logger)

if __name__ == '__main__':
    truncate_and_etl()