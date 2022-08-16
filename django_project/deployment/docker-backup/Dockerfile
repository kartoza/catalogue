FROM kartoza/pg-backup:v13---v20210523
MAINTAINER Rischan Mafrur <rischann@kartoza.com>

ADD backups.sh /backups.sh
RUN chmod 755 /backups.sh

CMD ["/start.sh"]
