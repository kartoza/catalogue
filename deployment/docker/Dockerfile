#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:3.8-buster AS base_image
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN apt-get update -y && \
    apt-get install -y openjdk-11-jre-headless
    
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN rm -rf $JAVA_HOME/lib/security && \
    ln -s $JAVA_HOME/conf/security $JAVA_HOME/lib/security

# Pandoc needed to generate rst dumps
RUN apt-get update -y && \
      apt-get -y install \
        yui-compressor \
        pandoc \
        build-essential \
        python3-all-dev \
        abiword \
        libreoffice-script-provider-python \
        libpq5 \
        python3-geoip \
        python3-pyproj \
        python3-lxml \
        gdal-bin gdal-data libgdal-dev \
        python3-gdal \
        nodejs npm --fix-missing

ADD libs /libs
ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install pyproj && pip install -r /REQUIREMENTS.txt && pip install uwsgi
RUN npm -g install yuglify

RUN sed -i "/        new_class = super_new(cls, name, bases, {'__module__': module})/a\        new_attrs = {'__module__': module}\n        classcell = attrs.pop('__classcell__', None)\n        if classcell is not None:\n            new_attrs['__classcell__'] = classcell\n        new_class = super_new(cls, name, bases, new_attrs)" /usr/local/lib/python3.8/site-packages/django/db/models/base.py

RUN sed -i "s/ver = geos_version().decode()/ver = geos_version().decode().split(' ')[0]/" /usr/local/lib/python3.8/site-packages/django/contrib/gis/geos/libgeos.py

ADD deployment/docker/uwsgi.conf /uwsgi.conf


# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

WORKDIR /home/web/django_project
COPY django_project /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]


#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM base_image AS dev_image
MAINTAINER Tim Sutton<tim@kartoza.com>

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# End of cut & paste section

ADD deployment/docker/REQUIREMENTS-dev.txt /REQUIREMENTS-dev.txt
RUN pip install -r /REQUIREMENTS-dev.txt
ADD deployment/docker/bashrc /root/.bashrc

# --------------------------------------------------------
# Open ports as needed
# --------------------------------------------------------

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
