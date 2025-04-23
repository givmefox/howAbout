from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking

end = datetime.now(timezone.utc)
start = end - timedelta(days=30)

run_ranking(start, end)
