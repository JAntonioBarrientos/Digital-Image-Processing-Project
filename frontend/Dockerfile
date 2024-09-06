# 1. Imagen base con Node.js
FROM node:18 AS build

# 2. Directorio de trabajo en el contenedor
WORKDIR /app

# 3. Copiar package.json y package-lock.json
COPY package*.json ./

# 4. Instalar dependencias
RUN npm install

# 5. Copiar el resto del código
COPY . .

# 6. Construir la aplicación
RUN npm run build

# 7. Usar una imagen de Nginx para servir la app
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# 8. Exponer el puerto en el contenedor
EXPOSE 80

# 9. Comando por defecto para ejecutar el contenedor
CMD ["nginx", "-g", "daemon off;"]
