import pywikibot
import pandas as pd
from pathlib import Path
from ast import literal_eval

import time


fpath = Path("vaccine_data").glob('**/*.csv')


files = [x for x in fpath if x.is_file()]

with open("old_schema.txt",'r') as f:
    old_schema = f.read() 

with open("new_schema.txt",'r') as f:
    new_schema = f.read()   

def header_fixer(pout):

    pmod = pout.split('"data":')[0]+'"data":'
    wdata = literal_eval(pout.split('"data":')[1][:-1])
    if old_schema in pmod:
        updt_pmod = pmod.replace(old_schema, new_schema)
        updt = 0
    else:
        updt_pmod = pout[:-2]
        updt = 1

    return updt_pmod, updt, wdata  

def string_data(file, wdata):


    df = pd.read_csv(file)
    df2 = df[['date', 'covishield',	'covaxin', 'sputnik', 'corbevax',
        'covovax','Total dose 1', 'Total dose 2', 'Total Precuation dose' ]]
    
    if len(wdata[0]) != len(df2.columns):
        diff_json = df2.to_json(orient="values")
    else:
        wdf = pd.DataFrame(wdata, columns=df2.columns)

        merge_df = pd.merge(df2,wdf, on=list(df2.columns), how='inner')
        df_diff = df2[~df2['date'].isin(merge_df['date'])]
        if df_diff.empty:
                diff_json = 0
        else:
                diff_json = df_diff.to_json(orient="values")
    return diff_json


def main(district):

    site = pywikibot.Site('commons', 'commons')  
    if district == 'kerala':
        page = pywikibot.Page(site, 'Data:COVID-19/Vaccinations/India/Kerala.tab')
    else:
        page = pywikibot.Page(site, f'Data:COVID-19/Vaccinations/India/Kerala/{district}.tab')

    

    text = page.text

    pmod, updt, wdata = header_fixer(text)

    covid_json = string_data(files[-1], wdata)

    if covid_json !=0 :
        if updt == 0:

            page.text = pmod + covid_json + "}"
            page.save('Replacing data')
        elif updt == 1:
            pmod += "," + covid_json[1:] + "}"
            page.text = pmod
            page.save('Replacing data')
            


if __name__=="__main__":

    for dist in files:
        district = dist.stem
        print(district)
        main(district)
        time.sleep(5)
