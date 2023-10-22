# 0) Dataset 💧🌎

Nos basamos en el dataset de Kaggle: [Water Quality](https://www.kaggle.com/datasets/adityakadiwal/water-potability).

Fue el utilizado para entrenar el modelo de la semana 7: Fastapi.
<br>Así que usen el modelo `rf.pkl` y las columnas del get dummies `categories_ohe.pkl`.

# 1) Consideraciones para el Docker

- Van a utilizar el puerto **5000**. 
- No olviden el tema del manejo de paths.
    ```python
    import os
    MAIN_FOLDER = os.path.dirname(__file__)
    MODEL_PATH = os.path.join(MAIN_FOLDER, "model/rf.pkl")
    COLUMNS_PATH = os.path.join(MAIN_FOLDER, "model/categories_ohe.pickle")
    ``` 
- Llamen a su imagen como `proyecto_bootcamp_edvai_jueves`.
