SELECT addr.addr_parsed address,
  APNO,
  APTYPE,
  EXAMINERAPPROVED as EXAMINER,
  NOPAGES,
  APDTTM
FROM PLAN_APP_PERMIT_NO_LNIADDR_MVW p,
  lni_addr addr
WHERE p.addrkey = addr.addrkey