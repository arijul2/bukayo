FROM nginx:alpine

# Copy nginx configuration files
COPY ./common.conf /etc/nginx/common.conf
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Create the .well-known directory and copy the apple-app-site-association file
RUN mkdir -p /usr/share/nginx/html/.well-known
COPY ./apple-app-site-association /usr/share/nginx/html/.well-known/apple-app-site-association

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html

# Expose port 80
EXPOSE 80