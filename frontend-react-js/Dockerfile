FROM node:16.18

ENV port=3000

WORKDIR /app

COPY ./package*.json /app

RUN npm install --silent

COPY . /app

EXPOSE ${PORT}

CMD ["npm","start"]
