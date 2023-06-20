import os
import pickle
import pandas as pd
import uvicorn

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI()

HOST = '127.0.0.1'
PORT = 7860

THRESHOLD = 0.37
MAIN_FOLDER = os.path.dirname(__file__)

# Model
model_filepath = "data/modelo_proyecto_final.pkl"
MODEL_PATH = os.path.join(MAIN_FOLDER, model_filepath)
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Columnas
columns_filepath = "data/categories_ohe_without_fraudulent.pkl"
COLUMNS_PATH = os.path.join(MAIN_FOLDER, columns_filepath)
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

# Bins - Order Amount
bins_order_filepath = "data/saved_bins_order_amount.pkl"
BINS_ORDER_PATH = os.path.join(MAIN_FOLDER, bins_order_filepath)
with open(BINS_ORDER_PATH, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)


class Request(BaseModel):
    orderAmount: float
    orderState: str
    paymentMethodRegistrationFailure: str
    paymentMethodType: str
    paymentMethodProvider: str
    paymentMethodIssuer: str
    transactionFailed: str
    emailDomain: str
    emailProvider: str
    customerIPAddressSimplified: str
    sameCity: str


@app.get("/")
async def root():
    return {"message": "Proyecto final para el Bootcamp de EDVAI"}


@app.post("/prediccion")
def predict_fraud_customer(request: Request):
    request_dict = jsonable_encoder(request)
    for key, value in request_dict.items():
        request_dict[key] = [value]

    # Generate pandas DataFrame
    single_instance = pd.DataFrame.from_dict(request_dict)

    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(
        float
    )
    single_instance["orderAmount"] = pd.cut(
        single_instance['orderAmount'],
        bins=new_saved_bins_order,
        include_lowest=True,
    )

    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance)
    single_instance_ohe = single_instance_ohe.reindex(columns=ohe_tr).fillna(0)

    # Prediction
    # prediction = model.predict(single_instance_ohe)
    # score = int(prediction[0])
    # return {"score": score}
    prediction_proba = model.predict_proba(single_instance_ohe)

    # Apply threshold
    is_fraudulent = True if prediction_proba[:, 1] >= THRESHOLD else False

    return {"is_fraudulent": is_fraudulent}


# Corre en http://127.0.0.1:7860 o http://0.0.0.0:7860
if __name__ == '__main__':
    # 0.0.0.0 o 127.0.0.1
    uvicorn.run(app, host=HOST, port=PORT)
