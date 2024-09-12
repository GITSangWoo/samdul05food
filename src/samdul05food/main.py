from fastapi import FastAPI
from typing import Union
from datetime import datetime 
import os 
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "n05"}

@app.get("/food")
def food(name:str):
    # 시간을 구함
    time = datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    home_path = os.path.expanduser('~')
    file_path=f"{home_path}/data/foodapp/data.csv"
    data_path=f"{home_path}/data/foodapp/"
    if os.path.exists(file_path):
        df=pd.read_csv(file_path)     
    else :
        df=pd.DataFrame(
            {
            'food' : [],
            'time': [],
            }
        )
    df.loc[len(df)] = [name,time]
    os.makedirs(os.path.dirname(data_path), exist_ok = True)
    df.to_csv(file_path,index=False)
    
    
    return {"food":name, "time": time }


