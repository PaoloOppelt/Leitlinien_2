# syntax=docker/dockerfile:1

# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Bundle app source
COPY . .

# Build your app
RUN npm run build

# Your app now uses a build folder with static files.
# Use a server to serve these files. In this example, we'll use serve.
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000
ENV HOST=0.0.0.0
# Run serve when the container launches
# CMD ["npm", "start"]
CMD ["serve", "-s", "build", "-l", "3000"]

