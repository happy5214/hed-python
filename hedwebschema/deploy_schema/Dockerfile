FROM python:3.6.5-alpine3.7
COPY ./requirements.txt /root/
WORKDIR /root
RUN apk add --no-cache gcc \
linux-headers \
musl-dev \
openrc \
libxslt-dev \
libxml2-dev \
apache2 \
apache2-dev && \
pip3 install --upgrade pip && \
pip3 install -r requirements.txt
COPY ./httpd.conf /etc/apache2/httpd.conf
COPY ./hedtools /var/www/hedtools/
RUN mkdir -p /run/apache2 && \
mkdir -p /var/log/hedtools && \
chown -R apache:apache /var/log/hedtools
ENTRYPOINT /usr/sbin/httpd -D FOREGROUND -f /etc/apache2/httpd.conf
ENV HEDTOOLS_CONFIG_CLASS=config.ProductionConfig
