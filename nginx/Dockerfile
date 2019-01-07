FROM nginx

# Copy the custom nginx config to sites available
COPY nginx.conf /etc/nginx/nginx.conf
COPY django_nginx.conf /etc/nginx/sites-available/
COPY uwsgi_params /etc/nginx/uwsgi_params

# Enable the custom nginx config
RUN mkdir -p /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled/

# Start nginx
CMD ["nginx", "-g", "daemon off;"]