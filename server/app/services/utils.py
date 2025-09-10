import re

_ACTIVE_VERBS = {"led","built","designed","improved","reduced","launched","delivered","optimized","implemented"}

def ats_checks(text: str) -> tuple[int, list[dict]]:
    checks = []
    t = text.lower()
    checks.append({"name":"Has contact (email)", "ok": bool(re.search(r"[\w.-]+@[\w.-]+", t))})
    checks.append({"name":"Has skills section", "ok": "skills" in t})
    checks.append({"name":"Uses active verbs", "ok": any(v in t for v in _ACTIVE_VERBS)})
    checks.append({"name":"Has numbers", "ok": bool(re.search(r"\b\d+%?|\$\d+", t))})
    ok_count = sum(1 for c in checks if c["ok"])
    score = int(100 * ok_count / len(checks))
    return score, checks
