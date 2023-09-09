# Use a Node.js base image
FROM node:20.3.0

# Set the working directory inside the container [prevents unnecessary reloads]
WORKDIR /app

# Copy the package.json and package-lock.json files first
# This is to take advantage of Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the container
COPY . .

# Expose the port on which your Vite server is running (5000 in this case)
EXPOSE 5000

# Start the development server
CMD ["npm", "run", "dev"]