FROM python:3.7-alpine3.9

MAINTAINER "BlueDynamics Alliance" http://bluedynamics.com
LABEL plone="5.2" \
    os="alpine" \
    os.version="3.9" \
    name="Plone 5.2" \
    description="Plone base image"


# Install OS
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    zlib-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libxml2-dev \
    libxslt-dev \
    pcre-dev \
    libffi-dev\
    git

# Add user
RUN addgroup -g 500 plone \
 && adduser -S -D -G plone -u 500 plone


# "git clone" is cached, we need to invalidate the docker cache here
ADD http://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new uuid


# Prepare data directory
# var/ is excluded from context via .dockerignore
RUN mkdir -p /data/blobstorage /data/filestorage
RUN mkdir -p /plone/var
RUN ln -s /data/blobstorage /plone/var/blobstorage
RUN ln -s /data/filestorage /plone/var/filestorage


# Install Plone
COPY . /plone
RUN pip install virtualenv
RUN virtualenv --clear /plone \
  && /plone/bin/pip install -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt \
  && /plone/bin/buildout -Nc /plone/docker.cfg


# Cleanup
RUN find /plone -name .git|xargs rm -rf \
  && find /plone -name *.pyc|xargs rm -rf \
  && find /plone -name *.pyo|xargs rm -rf
RUN apk del .build-deps \
  && apk add --no-cache --virtual .run-deps \
    su-exec \
    bash \
    rsync \
    libxml2 \
    libxslt \
    libjpeg-turbo \
  && rm -rf /plone/buildout-cache/downloads/*


# Final steps
RUN  chown -R plone.plone /plone /data

VOLUME /data
WORKDIR /plone
USER plone
EXPOSE 8080

HEALTHCHECK --interval=1m --timeout=5s --start-period=1m \
  CMD nc -z -w5 127.0.0.1 8080 || exit 1

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["start"]
