# Use an official Node runtime as the parent image
FROM node:lts

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the current directory contents into the container
COPY . .

# Build the Next.js app
RUN npm run build

# Set the command to run the app
CMD ["npm", "start"]
