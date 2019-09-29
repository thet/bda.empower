FROM registry.bluedynamics.eu/bda/plone-docker/plonebase:5.2-py3-latest

MAINTAINER "BlueDynamics Alliance" http://bluedynamics.com

# This suppresses a bunch of annoying warnings from debconf
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y \
        traceroute \
        iputils-ping \
        net-tools

RUN mkdir -p /plone /home/plone/.ssh

# this might be solved more elegant
COPY ./docker_id_rsa /home/plone/.ssh/id_rsa

RUN  ssh-keyscan git.bluedynamics.eu > /home/plone/.ssh/known_hosts

RUN  chown -R plone /home/plone/.ssh \
  && chmod 0600 /home/plone/.ssh/id_rsa \
  && chmod 0600 /home/plone/.ssh/known_hosts

# the "git clone" is cached, we need to invalidate the docker cache here
ADD http://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new uuid

COPY . /plone/buildout
RUN  chown -R plone /plone/buildout \
  && sudo -u plone virtualenv --clear /plone/buildout \
  && sudo -u plone /plone/buildout/bin/pip install -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt \
  && sudo -u plone /plone/buildout/bin/buildout -Nc /plone/buildout/docker.cfg \
  && find /plone/buildout -name .git|xargs rm -rf \
  && find /plone/buildout -name *.pyc|xargs rm -rf \
  && find /plone/buildout -name *.pyo|xargs rm -rf

USER plone

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["start"]
