FROM python:3.9-slim

WORKDIR /app

COPY ./backend-flask/requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


EXPOSE ${PORT}

COPY ./backend-flask .

CMD ["python3","-m","flask","run","--host","0.0.0.0","--port","5000"]