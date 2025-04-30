from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import json
import sys
# 📅 지난 7일간
sys.stdout.reconfigure(encoding="utf-8")
end = datetime.now(timezone.utc)
start = end - timedelta(days=7)

# 🟢 결과 반환
result = run_ranking(start, end)

# ✅ JSON만 출력
print(json.dumps(result, ensure_ascii=False))
