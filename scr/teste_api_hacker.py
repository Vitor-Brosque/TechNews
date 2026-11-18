from datetime import timedelta
from time import localtime

import httpx
from datatime import datetime, timezone

url = "http://hn.algolia.com/api/v1/http://hn.algolia.com/api/v1/search_by_date?"

n = 1

inicio = datetime(timezone.utc)
fim = inicio - timedelta(days=1)
print(localtime())

params = {
    "tags": "story",
    "numericFilters": "created_at_i>={},created_at_i<{}",
    "page": n,
}

response = httpx.get(url, params=params)

print(response.raise_for_status())
