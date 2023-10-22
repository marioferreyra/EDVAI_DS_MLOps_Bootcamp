# 1) Cargamos los datos 📕

```python
data = pd.read_csv("data/ohe_customer_dataset.csv", sep=",")
```

**Aclaración:** Podrían analizar todas las columnas, pero en este caso nos parece relevante solo analizar algunas columnas:

```python
filter_data = data[[
    "orderState_failed", "orderState_fulfilled", "orderState_pending",
    "transactionFailed", "fraudulent", "customerIPAddressSimplified_digits_and_letters"
]].copy()
```

# 4) Clustering con K-Means 🎯

Haremos todo el análisis para el dataframe `filter_data`

## 4.2) Creación del modelo

- Consideren `n_clusters=3

## 4.4) Analizando el modelo final: Gráfico de coordenadas`

**Generen 3 insights que les llamo la atención a partir del gráfico**

## Bonus: Scatter 3D!

En este caso como son pocas filas, no es necesario extraer una muestra.

Consideren `x='orderState_failed'`, `y='customerIPAddressSimplified_digits_and_letters'`, `z='transactionFailed', color='fraudulent'`

# 5) Clustering con HDBSCAN 🤖

## 5.2) Tuning/regularización de HDBSCAN para menos clusters

- Consideren `min_cluster_size=15`

## 5.3) Análisis del modelo cluster (profiling)

**Generen 3 insights que les llamo la atención a partir del gráfico**
