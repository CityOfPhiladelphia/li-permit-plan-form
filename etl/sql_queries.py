class SqlQuery():
    def __init__(self, extract_query_file, source_db, target_table):
        self.extract_query_file = 'queries/' + extract_query_file
        self.source_db = source_db
        self.target_table = target_table


PlanAppPermit = SqlQuery(
    extract_query_file='plan_app_permit.sql',
    source_db='GISLNI',
    target_table='eclipse_plan_app_permit'
)


PlanAppPlanPermitApnoToChar = SqlQuery(
    extract_query_file='plan_app_plan_permit_apno_tochar.sql',
    source_db='PERMITP',
    target_table='eclipse_plan_app_plan_permit'
)

queries = [PlanAppPermit]