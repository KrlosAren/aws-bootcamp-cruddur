# Week 1 — App Containerization


## Container Backend

Add Dockerfile into ./backend-flask

```
FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


EXPOSE ${PORT}

COPY . .

CMD ["python3","-m","flask","run","--host","0.0.0.0","--port","5000"]

```

### Build Container

Into root of project, we build backend image with the name backend

```sh
docker build --name backend ./backend-flask
```

### Run Container

```sh
docker run --rm -d --name backend -p 4500:5000 backend
```

With that command we run backend container in detach mode 
and expose port 4500.


## Container Frontend


Add Dockerfile into ./frontend-react-js

```
FROM node:16.18

ENV port=3000

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./package*.json /app

RUN npm install

COPY . /app

EXPOSE ${PORT}

CMD ["npm","run","start"]

```

### Build Container

Into root of project, we build backend image with the name frontend

```sh
docker build --name frontend ./frontend-react-js
```

### Run Container

```sh
docker run --rm -d --name frontend -p 3000:3000 frontend
```

With that command we run backend container in detach mode 
and expose port 3000.

## Add Docker Compose to run Multiples Container

Add this file docker-compose.yml in root of the app

```
version: "3.8"

services:

  backend:
    build:
      context: ./backend-flask
      dockerfile: Dockerfile
    container_name: backend_flask
    image: backend_flask
    volumes:
      - ./backend-flask:/app:z
    ports:
      - "4500:5000"
    environment:
      FRONTEND_URL : "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL : "https://4500-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      

  frontend:
    build:
     context: ./frontend-react-js
     dockerfile: Dockerfile
    container_name: frontend_react
    image: frontend_react
    volumes:
      - ./frontend-react-js:/app:z
    ports:
      - "3000:3000"
    environment:
      REACT_APP_BACKEND_URL : "https://4500-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"

networks: 
  internal-network:
    driver: bridge
    name: cruddur
```

With this file can be run multiples container at same time, the containers named services are backend and fronted

### Build containers

```sh
docker-compose build
```

### run container in detach mode

```sh
docker-compose up -d
```

### watch logs
```sh
docker-compose logs -f
```

### Get down the containers
```sh
docker-compose down
```

## Run Postgrest and DynamoDb

Add these container in docker-compose.yml

```
  dynamodb-local:
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local"
    container_name: dynamodb-local
    ports:
     - "8000:8000"
    volumes:
       -  ./docker/dynamodb:/home/dynamodblocal/data
    working_dir: /home/dynamodblocal
  
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes:
      - db:/var/lib/postgresql/data

```