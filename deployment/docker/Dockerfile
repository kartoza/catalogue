#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:2.7.18-buster AS base_image
MAINTAINER Tim Sutton<tim@kartoza.com>

# Pandoc needed to generate rst dumps
RUN apt-get update -y && \
      apt-get -y install \
        yui-compressor \
        pandoc \
        build-essential \
        python-all-dev \
        abiword \
        libreoffice-script-provider-python \
        libpq5 \
        python-geoip \
        gdal-bin gdal-data libgdal-dev \
        python-gdal --fix-missing


ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

ADD deployment/docker/uwsgi.conf /uwsgi.conf


# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

WORKDIR /home/web/django_project
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
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

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
