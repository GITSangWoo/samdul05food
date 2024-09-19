from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from datetime import datetime 
from pytz import timezone
import pymysql 
import os 
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8899",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_path():
    file_path=__file__
    dirpath = os.path.dirname(file_path)
    return dirpath
    

@app.get("/")
def read_root():
    return {"Hello": "n05"}

@app.get("/food")
def food(writername:str,foodname:str):
    # 시간을 구함
    time = datetime.now(timezone('Asia/Seoul'))
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    data_path=os.path.join(get_path(),"food05data")
    file_path=f"{data_path}/food05.csv"
    if os.path.exists(file_path):
        df=pd.read_csv(file_path)     
    else :
        df=pd.DataFrame(
            {
            'writer' :[],
            'food' : [],
            'time': [],
            }
        )
    df.loc[len(df)] = [writername,foodname,time]
    os.makedirs(data_path, exist_ok = True)
    df.to_csv(file_path,index=False)
    # DB 저장 
    conn = pymysql.connect(host='172.17.0.1', port=13306, user='food', password='1234', db='fooddb', charset='utf8')
    cur =  conn.cursor(pymysql.cursors.DictCursor) 
    query = "INSERT INTO foodhistory(username, foodname,dt) VALUES (%s, %s, %s)"
    cur.execute(query,(writername,foodname,time))
    conn.commit()

    return {"writer":writername,"food":foodname, "time": time }


