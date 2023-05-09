# Para el Entrenamiento (train)

## 0) Dataset 💧🌎

Nos basamos en el dataset de Kaggle: [Water Quality](https://www.kaggle.com/datasets/adityakadiwal/water-potability).

## 1) Preparación de datos
- Discreticen por igual frecuencia e igual rango las columnas: `ph`, `Sulfate` y `Trihalomethanes`.

- Agregar categoría `desconocido` a los valores NaN de las 3 columnas previamente mencionadas.

- Hacer un `get dummies`.

## 2) Clasificación
- Su variable target o de interés a clasificar es `Potability`.

- Recuerden comentar y NO utilizar la siguiente celda:
    ```python
    data_x = data_x.values
    data_y = data_y.values
    ``` 

- Utilicen el 30% del dataset para test.

- Para el Random Forest consideren los parámetros `n_estimators = 1000` y `random_state = 99`

- Guarden el modelo con el nombre `rf.pkl`.

- Guarden el nombre de las columnas
  ```python
    import pickle

    # Guardamos las columnas x (sin Potability)
    with open('categories_ohe.pickle', 'wb') as handle:
        pickle.dump(data_x.columns, handle, protocol=pickle.HIGHEST_PROTOCOL)
  ```

# Para la llamada a la API (call_api.py)
- Consideren esta data para el campo `data` del request
    ```json
    data = {
        'ph': 0,
        'Hardness': 204.890455,
        'Solids': 20791.318981,
        'Chloramines': 7.300212,
        'Sulfate': 368.516441,
        'Conductivity': 564.308654,
        'Organic_carbon': 10.379783,
        'Trihalomethanes': 86.990970,
        'Turbidity': 2.963135,
    }
    ```


# Para la creación de la API (main.py)

- De la misma manera que cargan el modelo, carguen el nombre de las columnas.
<br>Coloquen estas líneas de código debajo del bloque de código que carga el modelo.
    ```python
    # Columnas
    COLUMNS_PATH = "model/categories_ohe.pickle"
    with open(COLUMNS_PATH, 'rb') as handle:
        ohe_tr = pickle.load(handle)
    ```

- Para Pydantic: Recuerden que sus 9 columnas son flotantes / float.

- Para el endpoint `/prediccion`, llamen a su función `predict_water_potability`

- Tienen que adaptar los datos de input respecto a los datos que recibe el modelo. Entonces tienen que agregarle / reformatear el nombre de las columnas.
    ```python
    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Reformat columns
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)
    
    prediction = model.predict(single_instance_ohe)
    ```

---
# Prueba de la API

Ahora que saben que está funcionando su API. 
<br>Varien el campo `data` del request y evaluen que les trae como response.

**Request 1**
```json
data = {
    'ph': 0,
    'Hardness': 204.890455,
    'Solids': 20791.318981,
    'Chloramines': 7.300212,
    'Sulfate': 368.516441,
    'Conductivity': 564.308654,
    'Organic_carbon': 10.379783,
    'Trihalomethanes': 86.990970,
    'Turbidity': 2.963135,
}
```
**Response 2**
```json
{'score': 0}
```

**Request 1**
```json
data = {
    'ph': 7.7984536762012135,
    'Hardness': 188.39494231709176,
    'Solids': 32704.569285770576,
    'Chloramines': 11.078872478914501,
    'Sulfate': 258.1911841475428,
    'Conductivity': 507.1786882733106,
    'Organic_carbon': 18.272439235274646,
    'Trihalomethanes': 85.17766213336226,
    'Turbidity': 4.107267203260775,
}
```

**Response 2**
```json
{'score': 1}
```