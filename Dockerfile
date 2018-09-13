FROM python:3.7.0-alpine3.8

WORKDIR /var/www/app

RUN apk add --no-cache bash curl findutils nginx=1.14.0-r1 supervisor=3.3.4-r1
RUN mkdir -p /run/nginx

COPY requirements.txt /var/www/app
RUN pip install -r requirements.txt

COPY --chown=nginx:nginx . /var/www/app

COPY .container/nginx.conf /etc/nginx/nginx.conf
COPY .container/nginx-site.conf /etc/nginx/conf.d/default.conf
COPY .container/supervisord.conf /etc/supervisord.conf

RUN rm -rf .container

EXPOSE 80

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-c", "/etc/supervisord.conf"]
