import sqlite3
from flask import Flask,jsonify,request
import pandas as pd
from collections import OrderedDict


app = Flask(__name__)



def read_excel_data():
    df = pd.read_excel('20210309_2020_1 - 4 (1) (1) (1) (1).xls')
    app_data = df.groupby('API WELL  NUMBER').agg({'OIL':'sum','GAS':'sum','BRINE':'sum'}).reset_index()
    
    # DB connecting
    conn = sqlite3.connect('Ohio.db')
    app_data.to_sql('quarterly_productiontbl',conn,if_exists='replace',index=False)
    conn.close()


@app.route('/data',methods=['GET'])
def get_data():
    well = request.args.get('well')
    print("well",well)
    conn = sqlite3.connect('Ohio.db')
    cursor = conn.execute('SELECT * FROM quarterly_productiontbl WHERE "API WELL  NUMBER" = ?', (well,))
    row_data = cursor.fetchone()
    conn.close()
    data_val = {
        "oil":row_data[1],
        "gas":row_data[2],
        "brine":row_data[3],
    }
    print(data_val)
    return jsonify(data_val)

   

if __name__ == '__main__':
    read_excel_data()
    app.run(port=8080)