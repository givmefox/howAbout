from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import sys
# 현재 시간 (UTC 기준)
sys.stdout.reconfigure(encoding="utf-8")
now = datetime.now(timezone.utc)
start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) - timedelta(days=1)
end = start + timedelta(days=2)

# 결과값 받아오기
result = run_ranking(start, end)

# ✅ 딱 JSON만 출력
import json
print(json.dumps(result, ensure_ascii=False))
