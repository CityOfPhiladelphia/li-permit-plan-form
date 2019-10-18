SELECT addr.addr_parsed address,
  APNO,
  APTYPE,
  EXAMINER,
  NOPAGES,
  APDTTM
FROM PLAN_APP_PERMIT_NO_LNIADDR_MVW p,
  lni_addr addr
WHERE p.addrkey = addr.addrkey
AND APDTTM      > '01-JUL-2019'
AND apdttm      < '18-OCT-2019'