import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 as sq
import numpy as np
from datetime import datetime



url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country', 'GDP_USD_millions']
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = f'/Users/nombauser/Desktop/Python Work/Coursera/{table_name}.csv'



def extract(url, table_attribs):
    df = pd.DataFrame(columns=table_attribs)
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')

    for i in rows:
        col = i.find_all('td')
        if len(col)!=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                    data_dict = {"Country": col[0].a.contents[0],
                                "GDP_USD_millions": col[2].contents[0]}
                    df1 = pd.DataFrame(data_dict, index=[0])
                    df = pd.concat([df,df1], ignore_index=True)
    return df

df = extract(url=url, table_attribs=table_attribs)



def transform(df):
    # Converting the column to a list for transformation process
    GDP_list = df.iloc[:,1].tolist()
    myList = []

    # Performing the transformation on the stringed figures
    for x in GDP_list:
        x = x.split(',')
        x = float(''.join(x))
        x = np.round(x/1000,2)
        myList.append(x)
    df['GDP_USD_millions'] = myList

    # Renaming the columns
    df = df.rename(columns={'GDP_USD_millions':'GDP_USD_Billions'})
    return df

df = transform(df=df)





def load_to_csv(df, csv_path):
    df.to_csv(csv_path)
    
#load_to_csv(df,csv_path)




def load_to_db(df, *sql_connection, table_name):
    sql_connection = sq.connect(db_name)
    df.to_sql(table_name, sql_connection, index=False, if_exists='replace')
    sql_connection.close()

load_to_db(df, table_name=table_name)


def run_query(query_statement, query_connection):
    pass


def log_progress(message):
    pass





