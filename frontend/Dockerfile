FROM node:14-slim

WORKDIR /user/src/app

COPY ./package.json ./

RUN npm install && \
    npm cache clean --force && \
    rm -rf /var/lib/apt/lists/* /tmp/*

COPY . .

EXPOSE 3000

CMD npm start




