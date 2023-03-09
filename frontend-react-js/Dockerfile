FROM node:16.18

ENV port=3000

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./frontend-react-js/package*.json /app

RUN npm install

COPY ./frontend-react-js /app

EXPOSE ${PORT}

CMD ["npm","run","start"]
