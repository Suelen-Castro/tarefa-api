FROM node:20-alpine
WORKDIR /app

# Instala somente as dependências de produção
COPY package*.json ./
RUN npm ci --omit=dev

COPY src ./src

ENV PORT=3000
EXPOSE 3000

# Executa com usuário sem privilégios (boa prática de segurança)
USER node
CMD ["node", "src/server.js"]
