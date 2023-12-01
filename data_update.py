import pandas as pd
import requests
import time
from pathlib import Path
from collections import defaultdict


def collect_data(key, dist, days):
    """
    """
    headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
    dist_data = defaultdict(list)
    for date in days:
        res = requests.get(f"https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id=17&district_id={dist}&date={date.strftime('%Y-%m-%d')}",headers=headers)
        
        if res.status_code == 200:
            res2 = res.json()
        elif res.status_code == 403:
            #print(key, date.strftime('%Y-%m-%d'), res.status_code)
            time.sleep(1)
            res = requests.get(f"https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id=17&district_id={dist}&date={date.strftime('%Y-%m-%d')}",headers=headers)
            if res.status_code == 200:
                res2 = res.json()
            #print(key, date.strftime('%Y-%m-%d'), res.status_code)
        
        data = res2['topBlock']['vaccination']
        
        dist_data['date'].append(date.strftime('%Y-%m-%d'))
        dist_data['daily'].append(data['today'])
        dist_data['male'].append(data['male'])
        dist_data['female'].append(data['female'])
        dist_data['others'].append(data['others'])
        try:
            dist_data['Total dose 1'].append(data['tot_dose_1'])
        except KeyError:
            dist_data['Total dose 1'].append(0)
        try:
            dist_data['Total dose 2'].append(data['tot_dose_2'])
        except KeyError:
            dist_data['Total dose 2'].append(0)
        
        try:
            dist_data['Total Precuation dose'].append(data['tot_pd'])
        except KeyError:
            dist_data['Total Precuation dose'].append(0)

        dist_data['covishield'].append(data['covishield'])
        dist_data['covaxin'].append(data['covaxin'])
        try:
            dist_data['sputnik'].append(data['sputnik'])
        except KeyError:
            dist_data['sputnik'].append(0)
        try:
            dist_data['zycov'].append(data['zycov'])
        except KeyError:
            dist_data['zycov'].append(0)
        try:
            dist_data['corbevax'].append(data['corbevax'])
        except KeyError:
            dist_data['corbevax'].append(0)
        try:
            dist_data['covovax'].append(data['covovax'])
        except KeyError:
            dist_data['covovax'].append(0)
        try:
            dist_data['gemcovacc'].append(data['gemcovacc'])        
        except KeyError:
            dist_data['gemcovacc'].append(0)
        try:
            dist_data['gemcovacc_om'].append(data['gemcovacc_om'])        
        except KeyError:
            dist_data['gemcovacc_om'].append(0)

        dist_data['total'].append(data['total'])

    return dist_data

if __name__=='__main__':

    headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
    days = pd.date_range('2021-03-08', '2023-11-28')

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
            dist_df.to_csv(dist_path + "/" + key + ".csv", mode='a', header=False,index=None)
        else:
            dist_df.to_csv(dist_path + "/" + key + ".csv", mode='w', header=True, index=None)
        time.sleep(1)  

