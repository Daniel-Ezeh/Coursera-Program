from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import sqlite3 as sq



url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
dirr = '/Users/nombauser/Desktop/Python Work/Coursera/Project/'
table_attribs = ['Name', 'MC_USD_Billion']
table_attribs_2 = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
db_name = 'Banks.db'
output_csv_name = 'Largest_banks_data.csv'
table_name = 'Largest_banks'



def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() # getting the current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(f'code_log.txt','a') as f:
        f.write(f'{timestamp} : {message}\n')







def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    df = pd.DataFrame(columns=table_attribs)
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    
    for i in rows:
        col = i.find_all('td')
        if len(col)!=0:
            x = col[1].text.strip()
            y = col[2].text.strip()
            data_dict = {
                'Name': x,
                'MC_USD_Billion': float(y)
                  }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
    return df


x = (extract(url, table_attribs))





def transform(df, csv_file_name):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    df_new = pd.DataFrame(columns=table_attribs_2)

    csv_path = dirr + csv_file_name
    dataframe = pd.read_csv(csv_path)
    dict = dataframe.set_index('Currency').to_dict()

    EUR = dict['Rate ']['EUR']
    GBP = dict['Rate ']['GBP']
    INR = dict['Rate ']['INR']

    # create a dictionary to use to pack the values 
    # df['MC_GBP_Billion'] = np.round(df['MC_USD_Billion']*GBP, 2)
    # df['MC_EUR_Billion'] = np.round(df['MC_USD_Billion']*EUR, 2)
    # df['MC_INR_Billion'] = np.round(df['MC_USD_Billion']*INR, 2)

    df['MC_GBP_Billion'] = [np.round(x*GBP,2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*EUR,2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*INR,2) for x in df['MC_USD_Billion']]
    
    return df


#df = (transform(x,'exchange_rate.csv'))
# print(df['MC_EUR_Billion'][4]) = 146.86




def load_to_csv(df, output_csv_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    output_path = dirr + output_csv_path
    df.to_csv(output_path)





def load_to_db(df, db_name, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

    sql_connection = sq.connect(db_name)
    df.to_sql(table_name, sql_connection, index=False, if_exists='replace')
    sql_connection.close()







def run_query(query_statement, db_name):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    ''' Here, you define the required entities and call the relevant
    functions in the correct order to complete the project. Note that this
    portion is not inside any function.'''

    print(query_statement)
    sql_connection = sq.connect(db_name)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)



log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df,'exchange_rate.csv')
log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, output_csv_name)
log_progress('Data saved to CSV file')
#sql_connection = sq.connect('World_Economies.db')

log_progress('SQL Connection initiated.')
load_to_db(df, db_name, table_name)

qs1 = 'SELECT * FROM Largest_banks'
log_progress(f'Data loaded to Database as table. Running the query: \n{qs1}')
run_query(qs1, db_name)

qs2 = 'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'
log_progress(f'Data loaded to Database as table. Running the query: \n{qs2}')
run_query(qs2, db_name)

qs3 = 'SELECT Name from Largest_banks LIMIT 5'
log_progress(f'Data loaded to Database as table. Running the query: \n{qs3}')
run_query(qs3, db_name)

log_progress('Process Complete.')
