# Frontend Dockerfile for React + Vite application
FROM node:20-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source files
COPY . .

# Accept build-time argument for API URL
ARG CAMPLY_API_URL
ENV CAMPLY_API_URL=$CAMPLY_API_URL

# Build the application
RUN npm run build

FROM nginx:alpine as production

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
