FROM node:16.18

ENV port=3000

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./package*.json /app

RUN npm install

COPY . /app

EXPOSE ${PORT}

CMD ["npm","run","start"]
