from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking

# 현재 시간 (UTC 기준)
print("🟡 ranking_today 시작!",flush=True)  # ✅ 테스트용 로그

now = datetime.now(timezone.utc)

# 어제 00:00부터 오늘 23:59:59까지 (2일치)
start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) - timedelta(days=1)
end = start + timedelta(days=2)

# 랭킹 계산
run_ranking(start, end)

print("🟡 ranking_today 끝끝!", flush=True)  # ✅ 테스트용 로그
