# 1) Cargamos los datos 📕

En este caso nuestro el dataset tiene una extensión .json
<br>Con pandas podemos leer un json y convertirlo a dataframe.

```python
customer_file = 'data/customers.json'
df_json_nested = pd.read_json(customer_file, lines= True)
```

```python
df_json_nested.head(3)
```

Como podemos observar es un json anidado.
<br>Por eso dentro de las columnas `orders`, `paymentMethods` y `transactions` hay más información tipo dictionary o json.
<br>En cambio la columna `fraudulent` tiene un solo valor como corresponde.

## 1.1) Desanidar las columnas 

Para eso vamos a trabajar las columnas de manera separada y cada una las vamos a convertir en un dataframe. Y posteriormente unir / hacer un merge de estos dataframe en uno solo.

- ### Customer Dataframe

Como podemos observar: el valor dentro de cada celda en `Customer` es un json.

```python
from pandas import json_normalize
```

```python
customers_df = json_normalize(df_json_nested['customer'])
```

```python
customers_df.head(3)
```

- ### Orders Dataframe

Como podemos observar el valor dentro de cada celda en `orders` es una lista.

```python
orders_nested = pd.DataFrame([md for md in df_json_nested["orders"]])

orders_list=[]
for index,row in orders_nested.iterrows():
    for order in row:
        if order != None:
            orders_list.append(order)           

orders_df = pd.DataFrame(orders_list)
```

```python
orders_df.head(3)
```

- ### Transactions Dataframe

Como podemos observar el valor dentro de cada celda en `transactions` es una lista.

```python
transactions_nested = pd.DataFrame([md for md in df_json_nested["transactions"]])

transactions_list=[]
for index,row in transactions_nested.iterrows():
    for transaction in row:
        if transaction != None:
            transactions_list.append(transaction)           
transactions_df = pd.DataFrame(transactions_list)
```

```python
transactions_df.head(3)
```

- ### Payment Dataframe

```python
#Creating a payment_methods dataframe:
payment_nested = pd.DataFrame([md for md in df_json_nested["paymentMethods"]])

payment_methods_list=[]
for index,row in payment_nested.iterrows():
    for order in row:
        if order != None:
            payment_methods_list.append(order)           
payment_methods_df = pd.DataFrame(payment_methods_list)
```

```python
payment_methods_df.head(3)
```

- ### Fraudulent Dataframe

```python
fraudulent_df = df_json_nested['fraudulent']
```

## 1.2) Unir / Mergear dataframes

```python
data = pd.concat([customers_df, orders_df, payment_methods_df, transactions_df, fraudulent_df], axis=1)
```

```python
data.head(3)
```

# 2) Transformación de columnas 🙌

Vamos a transformar los valores de algunas columnas que parecen únicos para que sean utilizables.

```python
status(data)
```

## 2.1) Columnas duplicadas

Podemos observar que hay columnas repetidas como ser `orderId` y `paymentMethodId`.

Alguna vez les puede pasar esta situación: donde tienen 2 colunas con el mismo nombre, quieren conservar la columna y eliminar los duplicados. 

Hay muchas formas de hacerlo como se puede apreciar en [Stackoverflow](https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns).
<br>Nosotros vamos a usar la siguiente:

```python
data = data.loc[:,~data.columns.duplicated()].copy()
```

```python
status(data)
```

## 2.2) customerEmail

Generalmente solemos recibir mail de clientes que utilizan servicios de mensajería como `@hotmail`, `@yahoo` y `@gmail`. Esos son los tipos de mail más comunes.
<br>Muchas veces ciertos clientes con intenciones maliciosas usan otro tipo de mail como ser `@u6n7x`, `@1jcfcxs7` o `@6eph`.

```python
data.head(3)
```

Vamos a clasificarlos como `hotmail`, `yahoo`, `gmail` y `weird`.
<br>**Aclaración:** Esto se puede hacer usando expresiones regulares (Regex) y funciones lambda también, pero es más práctico de seguir / entender lo que hace el programa de la siguiente manera:

```python
email_domains= []
mails= []
popular_providers = ['yahoo', 'gmail', 'hotmail']

for email in data['customerEmail']:
    try:
        """
        Si email = "edvai@yahoo.com"

        aux = yahoo.com
        mail = yahoo
        domain = com
        """
        aux = email.split('@')[1]
        domain = aux.split('.')[1]
        mail = aux.split('.')[0]
        
        if mail in popular_providers:
            mails.append(mail)
        else:
            mails.append('other')
        email_domains.append(domain)
        
    except:
        email_domains.append('weird')
        mails.append('weird')
        # print(email)
```

Las listas creadas las convertimos a columnas del dataframe:

```python
data['emailDomain'] = email_domains
data['emailProvider'] = mails
```

```python
data.head(3)
```

Eliminamos la columna `customerEmail`:

```python
data = data.drop(['customerEmail'], axis=1)
```

```python
data.head(3)
```

## 2.3) customerIPAddress

Por ejemplo, nuestro localhost es 127.0.0.1
<br>Según el protocolo, podemos llegar a tener una subnet mask 255.255.255.255 (la máxima cantidad de caracteres numéricos), es decir podes alcanzar una longitud de:

```python
longitudIP = len(255.255.255.255)
print(longitudIP)
# 15
```

Pero hay IPs más extensas (>15) que contienen letras por ejemplo: `67b7:3db8:67e0:3bea:b9d0:90c1:2b60:b9f0`

Entonces lo que vamos a hacer es crear 2 columnas nuevas dependiendo el tipo de IP: <br>`customerIPAddress` y `digits_and_letters`.

**Aclaración:** Esto se puede hacer usando expresiones regulares para buscar letras en vez de medir longitud y funciones lambda, pero es más práctico de seguir / entender lo que hace el programa de la siguiente manera:

```python
IP_addresses = []
for address in data['customerIPAddress']:

    # A veces lo toma como flotante al address
    aux_address = str(address)
    
    if len(aux_address) > 15:
        IP_addresses.append('digits_and_letters')
    else:
        IP_addresses.append('only_letters')

data['customerIPAddressSimplified'] = IP_addresses
```

```python
data.head(3)
```

Eliminamos la columna `customerIPAddress`

```python
data = data.drop(['customerIPAddress'], axis=1)
```

## 2.4) customerBillingAddress vrs. orderShippingAddress

Verificar que la compra se realizo desde tu ciudad, y no desde otra parte del mundo.

**Aclaración:** Esto se puede hacer usando expresiones regulares y funciones lambda, pero es más práctico de seguir / entender lo que hace el programa de la siguiente manera:

```python
def extract_city_name(name_column):
    city_list = []

    for address in data[name_column]:
        try:
            """
            Si address = "5493 Jones Islands\nBrownside, CA 51896"

            aux = "Brownside, CA 51896"
            city_with_number = "CA 51896"
            city = "CA"
            """
            aux = address.split('\n')[1]
            city_with_number = aux.split(', ')[1]
            city = city_with_number.split(' ')[0]
            
            city_list.append(city)
                
        except:
            # Sino aparece el nombre de la ciudad asignamos: unknown
            city_list.append("unknown")
    
    return city_list
```

```python
data["customerBillingAddress"] = extract_city_name("customerBillingAddress")
data["orderShippingAddress"] = extract_city_name("orderShippingAddress")
```

```python
data.head(3)
```

También podemos evaluar que la ciudad de `customerBillingAddress` y `orderShippingAddress` coinciden.

**Aclaración:** Esto se puede hacer usando funciones lambda o np.where, pero es más práctico de seguir / entender lo que hace el programa de la siguiente manera:

Vamos a considerar si una de las 2 address al momento de comparar es `unknown`, le asignaremos como resultado `unknown`. Si ambas coinciden asignaremos `yes` y caso contrario `no`.

```python
same_city = []

for index in range(len(data)):
    billing_address = data["customerBillingAddress"][index]
    order_address = data["orderShippingAddress"][index]

    response = "unknown"
    if billing_address != "unknown" and order_address != "unknown":
        if billing_address == order_address:
            response = "yes"
        else:
            response = "no"
    
    same_city.append(response)
```

```python
data["sameCity"] = same_city
```

Con las columnas `customerBillingAddress` y `orderShippingAddress` se podría hacer un diagrama de flujo o de conexiones geoespacial o representarlo en un mapa.
<br>Conforme nuestra cartera de clientes crezca y tengamos más ciudades, más posibles valores tomarán las columnas `customerBillingAddress` y `orderShippingAddress`. En cambio `sameCity` va a seguir teniendo los mismos 3 posibles valores.
<br>Bajo ese criterio  vamos a despreciar ambas columnas y solo conservaremos `sameCity`.

```python
data = data.drop(["customerBillingAddress", "orderShippingAddress"], axis = 1)
```

```python
data.head(3)
```

## 2.5) customerPhone

El número de teléfono prácticamente es un identificador único.
<br>Pero lo que se podría hacer es obtener el código de área para saber dónde está registrado el celular. 
<br>Por ejemplo: Un número "+54 9 261-1234-578", se podría extraer el primer número y buscar de qué país es. En este caso el +54 corresponde a Argentina y el 261 a la provincia de Mendoza.

Y de esa manera se podría corroborar que el número del usuario tiene una correspondencia con el país o ciudad donde reside la persona.

En este caso hay un universo de posibilidades en cómo se presenta el dato en `customerPhone` y no registra un patrón. Si tuvieramos más contexto podríamos conservar la columna.
<br>Por este motivo vamos a eliminar la columna:

```python
data = data.drop(['customerPhone'], axis=1)
```

```python
data.head(3)
```

## 2.6) Identificadores únicos

Muchas veces en este tipo de productos de prevención de fraude se busca reducir la fricción. Por eso tenemos distintos identificadores del dispositivo del usuario, tracking del producto, etc.

En este caso tenemos identificadores únicos en las columnas `customerDevice`, `orderId`, `transactionId` y `paymentMethodId`. Por esa razón los vamos a eliminar.

```python
data = data.drop(['customerDevice', 'orderId', 'transactionId', 'paymentMethodId'], axis=1)
```

```python
data.head(3)
```

```python
status(data)
```

# 3) Guardar dataset como csv 💾

Guardamos el dataset adaptado con extensión .csv

```python
filename = "data/customer_dataset.csv"
data.to_csv(filename, index = False)
```
