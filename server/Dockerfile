FROM node:20-alpine

WORKDIR /app

ARG SERVER_PORT

COPY package.json package-lock.json ./
RUN npm install
COPY . .

EXPOSE ${SERVER_PORT}

CMD ["npm", "run", "start"]
