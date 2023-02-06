# Use an official NGINX image as the base image
FROM nginx:alpine

# Copy the HTML file to the default NGINX directory
COPY ./web-app/index.html /usr/share/nginx/html/index.html

# Expose port 80 to allow incoming traffic
EXPOSE 80

# Run the NGINX command to start the server
CMD ["nginx", "-g", "daemon off;"]