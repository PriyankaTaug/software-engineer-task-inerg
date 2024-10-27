import sqlite3
from flask import Flask
import pandas as pd


app = Flask(__name__)



def read_excel_data():
    df = pd.read_excel('20210309_2020_1 - 4 (1) (1) (1) (1).xls')
    app_data = df.groupby('API WELL  NUMBER').agg({'OIL':'sum','GAS':'sum','BRINE':'sum'})
    
    # DB connecting
    conn = sqlite3.connect('Ohio.db')
    app_data.to_sql('quarterly_productiontbl',conn,if_exists='replace',index=False)
    conn.close()


   

if __name__ == '__main__':
    read_excel_data()
    app.run(port=8080)