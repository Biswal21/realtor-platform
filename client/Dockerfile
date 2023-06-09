FROM node:lts-alpine

WORKDIR /usr/app

COPY package*.json ./
COPY tsconfig.json ./

EXPOSE 3000
EXPOSE 3001

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --upgrade bash



CMD npm install -g npm@latest \
    && npm install \
    && npm run dev

