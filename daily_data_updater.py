import pandas as pd
import requests
import time
from pathlib import Path
from collections import defaultdict
from data_update import collect_data
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days = 1)

days = pd.date_range(end=yesterday, periods=7, freq='D')


headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}

res1 = requests.get("https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id=17&district_id=&date=2023-05-16",
        headers=headers, timeout=10).json()

districts = {}
districts['kerala'] =''
for i in res1['getBeneficiariesGroupBy']:
    districts[i['title']] = i['id']

for key, dist in districts.items():
    

    dist_data = collect_data(key, dist, days)

        
    dist_df = pd.DataFrame(dist_data)
    dist_path = 'vaccine_data'
    Path(dist_path).mkdir(parents=True, exist_ok=True)
    if Path(dist_path + "/" + key + ".csv").is_file():
        old_df = pd.read_csv(dist_path + "/" + key + ".csv")
        merged_df = pd.concat([old_df, dist_df]).drop_duplicates(['date'], keep='last')
        merged_df.to_csv(dist_path + "/" + key + ".csv", mode='w', header=True, index=None)