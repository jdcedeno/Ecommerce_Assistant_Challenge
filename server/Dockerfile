# Use the official Node.js base image
FROM node:20-alpine AS base

# Install Python and required dependencies
RUN apk add --no-cache python3 py3-pip build-base

# Set the working directory
WORKDIR /app

# Copy the server files
COPY package.json package-lock.json ./

# Install Node.js dependencies
RUN npm install

# Copy Python-related files
COPY ./rag_qa_llm ./rag_qa_llm

# Set up a Python virtual environment
WORKDIR /app/rag_qa_llm
RUN python3 -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Ensure the script uses the virtual environment's Python interpreter
ENV PATH="/app/rag_qa_llm/venv/bin:$PATH"

# Make query_llm.py executable
RUN chmod +x query_llm.py

# Return to the application root directory
WORKDIR /app

# Copy the rest of the application files
COPY ./server.js ./

# Expose the port the server will run on
EXPOSE 3000

# Command to run the server
CMD ["node", "server.js"]
