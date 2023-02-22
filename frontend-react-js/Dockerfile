FROM node:16.18

ENV port=3000

WORKDIR /app

COPY . /app
RUN npm install

EXPOSE ${PORT}

CMD ["npm","start"]
