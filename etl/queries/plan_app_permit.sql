SELECT address,
       apno,
       aptype,
       examiner,
       nopages,
       apdttm,
       systemofrecord
FROM (SELECT sub.*,
             ROW_NUMBER () OVER (
                 PARTITION BY apno
                 ORDER BY systemofrecord ASC --if the same permit is in both eclipse and hansen, pick the eclipse one. Is this right, is this what we should do?
             ) seq_no
      FROM (SELECT CAST (addr.base_address AS VARCHAR2 (500)) address,
                   p.permitnumber apno,
                   p.permitdescription aptype,
                   p.examinerapproved AS examiner,
                   NULL nopages,
                   p.dateadvanced apdttm,
                   'ECLIPSE' systemofrecord
            FROM mvw_plan_app_permit_no_lniaddr p,
                 eclipse_lni_addr addr
            WHERE p.addressobjectid = addr.addressobjectid (+)
            UNION
            SELECT CAST (addr.addr_parsed AS VARCHAR2 (500)) address,
                   apno,
                   aptype,
                   examinerapproved AS examiner,
                   nopages,
                   apdttm,
                   'HANSEN' systemofrecord
            FROM plan_app_permit_no_lniaddr_mvw p,
                 lni_addr addr
            WHERE p.addrkey = addr.addrkey
      ) sub
     )
WHERE seq_no = 1 --if the same permit is in both eclipse and hansen, pick the eclipse one