from li_dbs import GISLNI, GISLNIDBX
from sql_queries import queries
import petl as etl


class CursorProxy(object):
    '''Required to use petl with cx_Oracle https://petl.readthedocs.io/en/stable/io.html#databases'''
    def __init__(self, cursor):
        self._cursor = cursor
    def executemany(self, statement, parameters, **kwargs):
        parameters = list(parameters)
        return self._cursor.executemany(statement, parameters, **kwargs)
    def __getattr__(self, item):
        return getattr(self._cursor, item)


def get_cursor(conn):
    return CursorProxy(conn.cursor())


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


def send_email(failed):
    from email.mime.text import MIMEText
    from phila_mail import server

    recipientslist = ['dani.interrante@phila.gov',
                      'philip.ribbens@phila.gov',
                      'shannon.holm@phila.gov',
					  'jessica.bradley@phila.gov']
    recipientslist = ['philip.ribbens@phila.gov']
    sender = 'ligisteam@phila.gov'
    commaspace = ', '
    text = f'AUTOMATIC EMAIL \n' + '\nThe following tables on GISLNIDBX failed to update:\n\n' + ', \n'.join(failed) + '\n\nThis table supports the permit-plan-form application.'
    msg = MIMEText(text)
    msg['To'] = commaspace.join(recipientslist)
    msg['From'] = sender
    msg['X-Priority'] = '2'
    msg['Subject'] = 'Important Email'
    server.server.sendmail(sender, recipientslist, msg.as_string())
    server.server.quit()


def get_source_db(query):
    if query.source_db == 'GISLNI':
        return GISLNI.GISLNI
    elif query.source_db == 'GISLNIDBX':
        return GISLNIDBX.GISLNIDBX

		
def get_extract_query(query):
    with open(query.extract_query_file) as sql:
        return sql.read()


def etl_(query, logger):
    source_db = get_source_db(query)
    extract_query = get_extract_query(query)

    logger.info(f'{query.target_table} - extracting data into pickle file...')
    with source_db() as source:
        etl.fromdb(source, extract_query).topickle(f'temp/{query.target_table}.p')

    logger.info(f'{query.target_table} - loading data from pickle file...')
    with GISLNIDBX.GISLNIDBX() as target:
        etl.frompickle(f'temp/{query.target_table}.p').todb(get_cursor(target), query.target_table.upper())


def etl_process(queries):
    logger = get_logger()
    logger.info('---------------------------------')
    logger.info('ETL process initialized')

    failed = []

    for query in queries:
        try:
            logger.info(f'{query.target_table} - starting update.')
            etl_(query, logger)
            logger.info(f'{query.target_table} - successfully updated.')
        except:
            logger.error(f'ETL Process into GISLNIDBX.{query.target_table} failed.', exc_info = True)
            failed.append(query.target_table)

    logger.info('ETL process ended')

    if len(failed) > 0:
        send_email(failed)


def main():
    global queries
    etl_process(queries)


if __name__ == '__main__':
    main()