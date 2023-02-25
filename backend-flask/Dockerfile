FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


EXPOSE ${PORT}

COPY . .

CMD ["python3","-m","flask","run","--host","0.0.0.0","--port","5000"]