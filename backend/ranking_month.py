from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import json
import sys
sys.stdout.reconfigure(encoding="utf-8")
end = datetime.now(timezone.utc)
start = end - timedelta(days=30)

# ✅ 결과 반환받기
result = run_ranking(start, end)

# ✅ JSON만 출력하기 (중간에 print 메시지 없어야 백엔드에서 파싱 가능)
print(json.dumps(result, ensure_ascii=False))