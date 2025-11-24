FROM node:18-alpine
WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar código
COPY . .

# Exponer puerto de Vite
EXPOSE 5173

# Levantar Vite en modo dev
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
