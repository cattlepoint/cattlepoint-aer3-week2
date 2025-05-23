# Use the current GA “latest” NGINX alpine image (1.28.0 as of May 22 2025)
FROM nginx:alpine

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy the static files to the nginx html directory
COPY index.html /usr/share/nginx/html/index.html

# Set the default environment variables for the backend service
ENV CATTLEPOINT_BACKEND_PORT_8000_TCP_ADDR=localhost \
    CATTLEPOINT_BACKEND_PORT_8000_TCP_PORT=8000

# Exposes port 80 for the web server
EXPOSE 80
