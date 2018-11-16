truncate_query = """
    DELETE FROM plan_app_permit
"""

permit_extract = """
    SELECT
        DISTINCT addr.addr_parsed address,
        TRIM(bldg.apno) apno,
        defn.aptype,
        apstat.examiner,
        bldg.nopages,
        trn.trndttm apdttm
    FROM
        imsv7.apdefn@lidb_link defn,
        imsv7.ap@lidb_link ap,
        imsv7.aptrn@lidb_link trn,
        imsv7.apfee@lidb_link fee,
        imsv7.apbldg@lidb_link bldg,
        lni_addr addr
    WHERE
        AND defn.apdefnkey = ap.apdefnkey (+)
        AND bldg.apno = ap.apno
        AND ap.addrkey = addr.addrkey
        AND ap.apkey = trn.apkey
        AND fee.apfeekey = trn.apfeekey
        AND apbldg.apno IS NOT NULL
        AND fee.feedesc LIKE '%PERMIT FEE%'
        AND trn.trnamt > 0
"""

cloud_insert = """
    INSERT INTO plan_app_permit (
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