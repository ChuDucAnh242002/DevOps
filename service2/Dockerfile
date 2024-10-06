From node:10.19.0-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY app.js .

EXPOSE 3000

CMD ["node", "app.js"]