from typing import Union
import pickle
from fastapi import FastAPI
from fishmlserv.model.manager import get_model_path

app = FastAPI()

### 모델 불러오기
pkls=get_model_path()

with open(pkls[0], "rb") as f:
    fish_model1 = pickle.load(f)

with open(pkls[1], "rb") as f:
    fish_model5 = pickle.load(f)

with open(pkls[2], "rb") as f:
    fish_model15 = pickle.load(f)

with open(pkls[3], "rb") as f:
    fish_model25 = pickle.load(f)

with open(pkls[4], "rb") as f:
    fish_model49 = pickle.load(f)

@app.get("/")
def read_root():
    return {"Hello": "n05"}

@app.get("/food")
def food(name:str):
    # 시간을 구함
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    return {"food":name, "time":"2024-09-15 11:12:13"}





@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/fish")
def fish(length: float, weight: float):
    """
    물고기의 종류 판별기

    Args:

length (float): 물고기 길이(cm)
weight (float): 물고기 무게(g)

    Returns:

dict: 물고기 종류를 담은 딕셔너리

"""
    if length > 30.0 :
        prediction = "도미"
    else :
        prediction = "빙어"
    return {
            "prediction": prediction,
            "length": length,
            "weight": weight
           }


@app.get("/fish_ml_predictor")
def fish(n_neighbors:int,length:float, weight:float):
    """
    물고기의 종류 판별기

    Args:
        legth (float) : 물고기 길이(cm)\
        weight(float) : 물고기 무기(g)

    Returns:
        dict: 물고기 종류를 담은 딕셔너리

    """
    if n_neighbors == 1:
        a=fish_model1.predict([[length,weight]])
    elif n_neighbors == 5:
        a=fish_model5.predict([[length,weight]])
    elif n_neighbors == 15:
        a=fish_model15.predict([[length,weight]])
    elif n_neighbors == 25:
        a=fish_model25.predict([[length,weight]])
    elif n_neighbors == 49:
        a=fish_model49.predict([[length,weight]])

    if a == 1:
        prediction = "도미"
    else :
        prediction = "빙어"

    return {
                "n_neighbors" : n_neighbors,
                "prediction" : prediction,
                "length" : length,
                "weight": weight
            }

