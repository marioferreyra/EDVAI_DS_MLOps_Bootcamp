FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=5000"]
