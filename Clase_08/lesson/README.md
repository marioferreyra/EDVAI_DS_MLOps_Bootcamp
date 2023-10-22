# Para crear la imagen
```
docker build -t proyecto_bootcamp_edvai_martes .
```

**-t:** tags

# Para crear el container
```
docker run -p 8000:8000 -e ID_USER=Carlos123 proyecto_bootcamp_edvai_martes
```

**-p:** publish

**-e:** env -> Variable de entorno
