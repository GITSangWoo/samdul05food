from fastapi import FastAPI
from typing import Union
from datetime import datetime 
import os 
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
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
def food(name:str):
    # 시간을 구함
    time = datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    data_path=os.path.join(get_path(),"food05data")
    file_path=f"{data_path}/food05.csv"
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
    os.makedirs(data_path, exist_ok = True)
    df.to_csv(file_path,index=False)
    
    
    return {"food":name, "time": time }


