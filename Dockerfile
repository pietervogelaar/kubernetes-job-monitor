FROM python:3.7.0-alpine3.8

WORKDIR /var/www/app

RUN apk add --no-cache bash curl findutils nginx=1.14.2-r0 supervisor=3.3.4-r1 && \
    curl -sSO https://storage.googleapis.com/kubernetes-release/release/v1.11.1/bin/linux/amd64/kubectl && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/kubectl && \
    mkdir /etc/.kube && \
    touch /etc/.kube/config

COPY requirements.txt /var/www/app

RUN pip install -r requirements.txt && \
    mkdir -p /run/nginx

COPY --chown=nginx:nginx . /var/www/app

RUN mv .container/start.sh /start.sh && \
    chmod u+x /start.sh && \
    mv .container/nginx.conf /etc/nginx/nginx.conf && \
    chown root:root /etc/nginx/nginx.conf && \
    mv .container/nginx-site.conf /etc/nginx/conf.d/default.conf && \
    chown root:root /etc/nginx/conf.d/default.conf && \
    mv .container/supervisord.conf /etc/supervisord.conf && \
    chown root:root /etc/supervisord.conf && \
    rm -rf .container

EXPOSE 80

ENTRYPOINT ["/bin/bash"]
CMD ["/start.sh"]
