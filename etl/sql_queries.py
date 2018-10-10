truncate_query = """
    DELETE FROM permit
"""

permit_extract = """
    SELECT
        addr.addr_parsed address,
        TRIM(apstat.apno) apno,
        defn.aptype,
        apstat.examiner,
        apstat.apdttm
    FROM
        imsv7.imsv7li_permitappstatus@lidb_link apstat,
        imsv7.apdefn@lidb_link defn,
        imsv7.ap@lidb_link ap,
        lni_addr addr
    WHERE
        ap.apno = apstat.apno (+)
        AND defn.apdefnkey = ap.apdefnkey (+)
        AND ap.addrkey = addr.addrkey
        AND apstat.apno IS NOT NULL
"""

cloud_insert = """
    INSERT INTO permit (
        address,
        apno,
        aptype,
        examiner,
        apdttm
    ) VALUES (
        :1,
        :2,
        :3,
        :4,
        :5
    )
"""

# exporting queries
class SqlQuery:
    def __init__(self, extract_query, load_query):
        self.extract_query = extract_query
        self.load_query = load_query

# create instance of SqlQuery class
permit_to_cloud_query = SqlQuery(permit_extract, cloud_insert)