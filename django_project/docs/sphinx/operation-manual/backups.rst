

% Leave the above two lines blank please

== Backup systems ==

A number of backups are in place but it should be noted that there is cohesive
distaster recovery plan and system in place. In particular, there are no full
system images, there are no offsite backups and the ~26TB of online storage
connected to LION are not backed up. This document describes those backup
systems that are in place and that should be checked etc.

**We strongly recommend a complete disaster recovery solution be implemented.**


=== Nightly database dumps ===

=== Nightly Clone of sac live to sac-test ===

=== Nightly thumbs rsync ===

A duplicate tree of the catalogue thumbnails is stored on cheetah / cxfs at:

```
/cxfs/backups/lion/thumbnails_master_copy/
```

This tree is updated nightly via a cronjob running as the root user on cheetah.
The script for the cron job is listed below:

```
#/bin/bash

# This should be run in a cron job nightly by root to 
# Pull thumbs over from LION to mirror them on cxfs.
# Root needs to have rssh client key for lion configured - see 
# Catalogue documentation for details.
#
# You should add an entry like this to root's crontab to run this every night /
# week as you prefer. 
# e.g.
# Job will run 23:05 pm each day
#5 23 * * * /usr/local/bin/sac/mirror_catalogue_thumbs
#
#
cd /cxfs/backups/lion/thumbnails_master_copy/
rsync -ave ssh lion:/mnt/cataloguestorage/thumbnails_master_copy/. .
```


And the cronjob entry itself looks like this.

```
# Job will run at 23:05 each days to maintain a mirror of the catalogue thumbs
5 23 * * * /usr/local/bin/sac/mirror_catalogue_thumbs
```

**Note:** For the above to work, the filedrop configuration process must have
been followed (described elsewhere in this document)


**Note:** This backup is a mirror only, there is no rotating backup
implemented. SAC/SANSA are responsible to ensure that the cxfs is backed up
including this directory if proper long term offsite backups are to be had.

=== Nightly products rsync ===

Currently the online products **are not backed up**. Ultimately there should be
no online products store as everything should be in the DIMS product library,
and retrieved via the OGC Ordering Services for EO interface to DIMS.

Until such time, we **highly recommend** making a tape facility available so
that occasional snapshots can be made.

=== Nightly Mapping directory rsync ===

Currently the mapping data in /mnt/cataloguestorage/data is **not backed up**.
This data does not change very often. However it is quite voluminous. We
**highly recommend** that SAC should provide access to a tape drive so that
occasionally snapshots can be made.

=== System backups for Elephant ===

=== System backups for Lion ===


=== Backups pulled to cheetah / cxfs ===

**Note:** Please see the filedrop chapter which describes how rssh/ssh/filedrop
user is set up to allow passwordless scp and rsync operations to be carried
out.

==== Setup NTP ====

Firstly, you should ensure that the system time on cheetah is kept properly synchronised via ntp:

```
sudo /sbin/yast2
```

Now configure ntp according to the following two screenshots

[img/sac06.png]

[img/sac05.png]

==== Install the backup script ====

On cheetah the script is available at:

```
#/bin/bash

# This should be run in a cron job nightly by root to 
# Pull backups over from LION for the catalogue and GIS databases
# Root needs to have rssh client key for lion configured - see 
# Catalogue documentation for details.
#
# You should add an entry like this to root's crontab to run this every night /
# week as you prefer. Note the lion bacup cron job runs at 2:05 am so this 
# backup should be timed  for some time later.
# e.g.
# Job will run 7:05 am each day
#5 7 * * * /usr/local/bin/sac/fetch_pg_backups
#


cd /cxfs/backups/sql_backups/
MONTH=$(date +%B)
YEAR=$(date +%Y)
mkdir -p $YEAR/$MONTH
cd $YEAR/$MONTH
sudo scp lion:/mnt/cataloguestorage/backups/${YEAR}/${MONTH}/sac_postgis_`date +%d%B%Y`.dmp .
sudo scp lion:/mnt/cataloguestorage/backups/${YEAR}/${MONTH}/gis_postgis_`date +%d%B%Y`.dmp .

```

==== Add crontab entry ====

As directed abovem you should add a crontab entry e.g.:

```
sudo crontab -e
```

And then add this line:

```
# Job will run 7:05 am each day
5 7 * * * /usr/local/bin/sac/fetch_pg_backups
```
