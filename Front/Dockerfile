# ./Portfolio-project/Front/Dockerfile
FROM node:16-alpine

WORKDIR /app

# Copy the package.json and install dependencies
COPY package.json package-lock.json /app/
RUN npm install

# Copy the Angular project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 4200

# Run the Angular development server
CMD ["npm", "run", "start"]
