# Build Stage
FROM node:20-alpine AS build

# Install necessary dependencies for Alpine
RUN apk update && apk add --no-cache bash

WORKDIR /app

ARG VITE_API_URL

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the source code
COPY . .

# Run the TypeScript build
RUN npx tsc -b && npm run build

# Serve the build with Nginx
FROM nginx:alpine

# Copy the build output from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
