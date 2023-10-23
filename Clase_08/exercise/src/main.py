import os
import pickle
import pandas as pd
import uvicorn

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI()

HOST = '127.0.0.1'
PORT = 5000
MAIN_FOLDER = os.path.dirname(__file__)

# Model
MODEL_PATH = os.path.join(MAIN_FOLDER, "data/rf.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Columnas
COLUMNS_PATH = os.path.join(MAIN_FOLDER, "data/categories_ohe.pkl")
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)


class Answer(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float


@app.get("/")
async def root():
    return {"message": "Proyecto para Bootcamp de EDVAI"}


@app.post("/prediccion")
def predict_water_potability(answer: Answer):
    answer_dict = jsonable_encoder(answer)
    for key, value in answer_dict.items():
        answer_dict[key] = [value]

    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Reformat columns
    single_instance_ohe = pd.get_dummies(single_instance)
    single_instance_ohe = single_instance_ohe.reindex(columns=ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)

    # Cast numpy.int64 to just a int
    score = int(prediction[0])

    return {"score": score}


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
