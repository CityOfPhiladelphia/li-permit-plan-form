truncate_query = """
    TRUNCATE TABLE plan_app_permit_test
"""

permit_extract = """
    SELECT addr.addr_parsed address,
	  APNO,
	  APTYPE,
	  EXAMINER,
	  NOPAGES,
	  APDTTM
	FROM PLAN_APP_PERMIT_NO_LNIADDR_MVW p,
	  lni_addr addr
	WHERE p.addrkey = addr.addrkey
	AND APDTTM > '01-JUL-2019' and apdttm < '18-OCT-2019'
"""

cloud_insert = """
    INSERT INTO plan_app_permit_test (
    address,
    apno,
    aptype,
    examiner,
    nopages,
    apdttm
    ) VALUES (
    :1,
    :2,
    :3,
    :4,
    :5,
    :6
    )
"""

# exporting queries
class SqlQuery:
    def __init__(self, extract_query, load_query):
        self.extract_query = extract_query
        self.load_query = load_query

# create instance of SqlQuery class
permit_to_cloud_query = SqlQuery(permit_extract, cloud_insert)