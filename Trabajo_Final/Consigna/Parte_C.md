# Gradio 📍

## Diseño

**Son libres de crear y diseñar la interfaz gráfica.**
<br>Pueden inspirarse armando una interfaz gráfica similar a la siguiente:

![Interfaz gráfica](imgs/Captura%20web_5-6-2023_0584_127.0.0.1.jpeg)

## Recomendaciones

- De la misma manera que cargan el modelo, carguen el nombre de las columnas.
<br>Coloquen estas líneas de código debajo del bloque de código que carga el modelo.
    ```python
    COLUMNS_PATH = "model/categories_ohe_without_fraudulent.pickle"
    with open(COLUMNS_PATH, 'rb') as handle:
        ohe_tr = pickle.load(handle)
    ```
- También carguen sus puntos de corte / bins:
    ```python
    BINS_ORDER = os.path.join(MAIN_FOLDER, "model/saved_bins_order.pickle")
    with open(BINS_ORDER, 'rb') as handle:
        new_saved_bins_order = pickle.load(handle)

    BINS_TRANSACTION = os.path.join(MAIN_FOLDER, "model/saved_bins_transaction.pickle")
    with open(BINS_TRANSACTION, 'rb') as handle:
        new_saved_bins_transaction = pickle.load(handle)
    ```

- Tienen que adaptar los datos de input respecto a los datos que recibe el modelo. Entonces tienen que agregarle / reformatear el nombre de las columnas y los puntos de corte.
    ```python
    # Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)
    
    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
    single_instance["orderAmount"] = pd.cut(single_instance['orderAmount'],
                                     bins=new_saved_bins_order, 
                                     include_lowest=True)
    
    single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
    single_instance["transactionAmount"] = pd.cut(single_instance['transactionAmount'],
                                     bins=new_saved_bins_order, 
                                     include_lowest=True)
    
    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)
    ```

- Como sabemos el model nos devuelve los tipos de fraude 1, 2 y 3 en el response. Podemos devolver un response estilo semáforo.
    ```python
    # Cast numpy.int64 to just a int
    type_of_fraud = int(prediction[0])

    # Adaptación respuesta
    response = "Error parsing value"
    if type_of_fraud == 0:
        response = "False"
    if type_of_fraud == 1:
        response = "True"
    if type_of_fraud == 2:
        response = "Warning"
    ```

- Vamos a crear un endpoint para nuestra API llamado `api_name="prediccion"`

    ```python
    predict_btn.click(
                predict,
                inputs=[
                    orderAmount,
                    orderState,
                    paymentMethodRegistrationFailure,
                    paymentMethodType,
                    paymentMethodProvider,
                    paymentMethodIssuer,
                    transactionAmount,
                    transactionFailed,
                    emailDomain,
                    emailProvider,
                    customerIPAddressSimplified,
                    sameCity,
                ],
                outputs=[label],
                api_name="prediccion"
            )
    ```

## Para la llamada a la API (call_api.py)

- En Gradio a nuestro endpoint se le añade **/run**
  <br>Entonces deberíamos tener la siguiente url:
    ```python
    # No olvidar agregar endpoint /prediccion
    search_api_url = 'http://127.0.0.1:7860/run/prediccion'
    ```

- Consideren esta data para el campo `data` del request
    ```python
    # CASO 1 -> Tipo de fraude: 0/False
    data = {
        "data": [
            18.0,
            "pending",
            "True",
            "card",
            "JCB 16 digit",
            "Citizens First Banks",
            18,
            "False",
            "com",
            "yahoo",
            "only_letters",
            "yes"  
        ]
    }
    ```

- Ahora que saben que está funcionando su API. 
  <br>Varien el campo `data` del request y evaluen que les trae como response.

    ```python
    # CASO 2 -> Tipo de fraude: 1/True
    data = {
    "data": [
        26.0,
        "fulfilled",
        "True",
        "bitcoin",
        "VISA 16 digit",
        "Solace Banks",
        26,
        "False",
        "com",
        "yahoo",
        "only_letters",
        "no" 
        ]
    }
    ```

# Hugging Face Spaces 🎯

Hagan su despliegue de su interfaz gráfica en Hugging Face.

Y peguen el link de su proyecto acá: [Mario Ferreyra - EDVAI DS MLOps Bootcamp - Trabajo Final](https://huggingface.co/spaces/marioferreyra/edvai_ds_mlops_bootcampi_trabajo_final)
