FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package.json ./package.json
COPY frontend/package-lock.json ./package-lock.json

# Use npm install (npm ci has a crash bug on some Linux/Docker setups)
RUN npm install

# Copy source code
COPY frontend/ ./

# Build
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
