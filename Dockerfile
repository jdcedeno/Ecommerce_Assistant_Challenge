# Use a base image with both Node.js and Python
FROM node:20-bullseye

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy the application files
COPY package*.json ./
COPY server.js .
COPY script.py .

# Install Node.js dependencies
RUN npm install

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
