Configuring the database server
------------------------------------------

The database server is an IBM P5 64bit PPC architecture server. This section details 
the process for setup and configuration of Debian 4.0 'Woody' onto the server. The machine 
has since been upgraded to 'Lenny' (Debian 5.0) and will shortly be upgraded to 'Squeeze' 
(Debian 6.0). Not many linux distributions support PPC64 architecture. Debian is a good 
choice for this environment because:

- debian itself is an extremely stable and well regarded Linux distribution (it forms the basis 
  of many other distros such as Ubuntu).
- debian supports a wide range of architectures.
- free support is readily available via the debian-ppc channel on IRC (freenode).
- unlike Redhat and Suse, its almost trivial to upgrade from major release to major release and 
  is easy to keep current with security updates.
- there is a huge selection of software packages available easily via the efficient APT package
  archive so its rarely needed to compile software from source (which introduces software 
  maintenance hassles).
-

Initial Install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Software Raid Partitioning scheme on p5

+ Server has 4 * 170gb drives.
+ Server has 22gig ram
+

Reboot server from HMC (Hardware management console)

Press 5 when prompted with a menu so that it will boot from cdrom

Type ``install64``

at the boot prompt.

+ Choose install language: English
+ Choose country: South Africa
+ Choose a locale: en_ZA.utf8
+ Choose additional locales: none
+ Keymap for a USB keyboard: American English
+ Primary Network Interface: eth5
+ Network: press cancel durint autoconfigure with dhcp
+ Configure network manually
+ IP Address: 196.35.94.197
+ Netmask: 255.155.155.0
+ Gateway: 196.35.94.1
+ Nameserver: 168.210.2.2
+ Hostname: elephant
+ Domain Name: csir.co.za
+ Partitioning: Manual
+

We will set up following scheme (identical on each drive)

+ **Primary Partition 1**: 8.2mb bootable flag on, physical volume for PReP ppc
boot partition (we will clone this with dd across all devices since it cant
reside inside of a software raid device. The PReP partition must reside in the
first partition.  
+ **Primary Partition 2**: 11.5gb swap (we will stripe swap
across all drives for best performance) 
+ **Primary Partition 3**: 11 bootable
flag on,  for / partition - we will use ext3 and clone from sda3 to sdb3,sdc3
and sdd3 after setting up the OS 
+ **Primary Partition 4**: 124.8gb All remaining
space physical volume for raid (will become part of md0) for /opt partition -
we will use raid 5 (stripe with parity) with 3 active drives and 1 hotswap
drive.
+

After doing the above, choose software raid in the partitioning tool and do:

+ **md0**: /, rootfs formated to ext3 Raid 5 with Active drives: sda4, sdb4, sdc4  Hot Spare: sdd4
+

Save partition layout and continue:


+ Root Password: ______________________
+ Full Name of new user: Tim Sutton
+ Username for your account: timlinux
+ Password: _______________________
+ Installing the base system:
+ Use a network mirror? yes (use za mirror as prompted)
+ Choose software to install: Standard system only
+ Device for bootloader installation: /dev/sda1 (we will clone to other drives later with dd)
+ Reboot...
+

Install openssh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the server comes up from its post install reboot you should install key pieces of software 
on it, starting with ssh (secure shell).

``sudo apt-get install openssh-server``

Configure openssh to run on a non-standard port, only accept named users and
require public key authentication for added security. To do this edit 


``/etc/ssh/sshd_config``

And change / add the following values::

  Port 8697
  PermitRootLogin no
  #Add additional users who should have ssh access here delimited by spaces
  AllowUsers timlinux wluck rgremels cstephens
  Protocol 2
  ListenAddress 196.35.94.197
  RSAAuthentication yes
  PubkeyAuthentication yes
  PasswordAuthentication no 
  Banner /etc/sshbanner.txt

This forces ssh connections to only allow access to specific users on a non-standard 
port and using a public/private key pair.

Create this file as /etc/sshbanner.txt::
                     __     __
                    /  \~~~/  \    
              ,----(     ..    )   
             /      \__     __/   
           /|         (\  |(  
          ^ \   /___\  /\ |   hjw 
             |__|   |__|-"    `97 


                SAC Database Server

      Access to this computer is restricted to
                authorised personnel.


Now restart ssh:

```
sudo /etc/init.d/ssh restart
```

Setup system locales
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
sudo dpkg-reconfigure locales
```

- Select 'All Locales'
- Choose en_ZA.utf8 as the default locale
- Choose OK and wait while the locales are generated
- 

Upgrade to lenny
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The initial installation above was carried out using Debian 4.0 Stable 'Etch'.
Subsequently, Debian 5.0 'Lenny' was released and so I upgraded using the
following procedure:

Edit /etc/apt/sources.list as root and replace all 'etch' instances with 'lenny
so that it looks like this::

  # 
  # deb cdrom:[Debian GNU/Linux 4.0 r4a _lenny_ - Official powerpc NETINST Binary-1 20080804-15:15]/ lenny contrib main

  #deb cdrom:[Debian GNU/Linux 4.0 r4a _lenny_ - Official powerpc NETINST Binary-1 20080804-15:15]/ lenny contrib main

  deb http://debian.mirror.ac.za/debian/ lenny main
  deb-src http://debian.mirror.ac.za/debian/ lenny main

  deb http://security.debian.org/ lenny/updates main contrib
  deb-src http://security.debian.org/ lenny/updates main contrib

Note as well that we have commented out the CD rom sources so that only online
apt repositories are used.

Next I ran the following commands to perform the operating system upgrade::
  
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get dist-upgrade

Note this can take some time depending on bandwidth availability.

After the upgrade is completed you should reboot the system so that you 
are using the newly installed kernel.

Upgrade to squeeze
------------------------------------------

The Lenny installation above has since been superceded by debian 6 'squeeze'.
I upgraded using the following procedure:

Edit /etc/apt/sources.list as root and replace all 'etch' instances with 'lenny
so that it looks like this::

  # 
  # deb cdrom:[Debian GNU/Linux 4.0 r4a _squeeze_ - Official powerpc NETINST Binary-1 20080804-15:15]/ squeeze contrib main

  #deb cdrom:[Debian GNU/Linux 4.0 r4a _squeeze_ - Official powerpc NETINST Binary-1 20080804-15:15]/ squeeze contrib main

  deb http://debian.mirror.ac.za/debian/ squeeze main
  deb-src http://debian.mirror.ac.za/debian/ squeeze main

  deb http://security.debian.org/ squeeze/updates main contrib
  deb-src http://security.debian.org/ squeeze/updates main contrib

Note as well that we have commented out the CD rom sources so that only online
apt repositories are used.

Next I ran the following commands to perform the operating system upgrade::

   sudo apt-get update
   sudo apt-get upgrade
   sudo apt-get dist-upgrade


Note this can take some time depending on bandwidth availability.

After the upgrade is completed you should reboot the system so that you 
are using the newly installed kernel.

Firewall setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note: This procedure is update to reflect availability of ufw packages for Squeeze.

Note: updated for debian squeeze which now provides uncomplicated firewall
(ufw) packages.::

  sudo apt-get install ufw 
  sudo ufw allow 8697
  sudo ufw allow 5432
  sudo ufw allow from 127.0.0.1/32 to 0.0.0.0/0 port 25
  sudo ufw default allow outgoing
  sudo ufw default deny incoming
  sudo ufw status

8697 - ssh, 5432 postgresql, 25 outbound mail

Setup Postgres/Postgis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This system is running software RAID 0 (mirror) and is well suited as a
database server running postgres and PostGIS (the Spatial data extension for
postgres). We will balance the load between the two PPC64 servers so that one
is a dedicated database server and the other a dedicated web server. For web
pages that are dynamically created, the web server will make database requests
off the database server::

  sudo apt-get install postgresql-8.1 postgresql-8.1-postgis
  sudo su - postgres

Now as the postgres user make yourself a super user account and a read only user 
for mapserver::

  createuser -s -d -r -l -P -E -e timlinux
  createuser -S -D -R -l -P -E -e readonly
  exit

Enter prompts following above commands as needed. Now you have postgres
installed and a user created. Next create an empty spatial database:

**Note**: or see further below to restore existing backups of a dba

Next set up the gis db::
   
   createdb gis
   createlang plpgsql gis

Now load the postgis sql dump and the srs tables::

  psql sac < /usr/share/postgresql-8.1-postgis/lwpostgis.sql 
  psql sac < /usr/share/postgresql-8.1-postgis/spatial_ref_sys.sql 

From here you can use the shp2pgsql command line tool to load data into 
postgis, or a tool such as QGIS / udig etc to do it using a gui.

Lastly we need to enable postgis for TCP/IP access. First::

  sudo vim /etc/postgresql/8.1/main/pg_hba.conf

And add one entry at the bottom of the file per host that 
needs access. You can also add a subnet etc. See pg docs for 
more info on that. I will just add my desktop pc as a client.::

  # Next line added by Tim to enable django server machine to connect on TCP/IP
  host    all         all         /32        md5

If you wish to allow connections from a broader range of hosts (e.g. SANSA EO Staff),
you  can add a subnet e.g::

  # For internal sac users - wired lan
  host    all         all         41.74.144.0/24        md5

Also we need to allow tcp/ip connections from hosts other than 
localhost::

   sudo vim /etc/postgresql/8.1/main/postgresql.conf

And add this line::

  # Next line added by Tim to enable remote machines to connect on TCP/IP
  listen_addresses='*'


Also for performance tuning, set the following settings in the above file::

  #Changed by Tim for tuning
  # Changed again from 16mb to 6GB based on http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server
  # I.e. 1/4 ram (this server has 24GB)
  #I set it to 3GB as I get an error with anything over 3GB
  shared_buffers = 3GB #16MB # min 128kB or max_connections*16kB

  # Tweaked by Tim for performance
  # (see http://www.westnet.com/~gsmith/content/postgresql/pg-5minute.htm)
  effective_cache_size = 12GB

  # Tweaked by tim based on http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server
  work_mem = 256MB                                # min 64kB

Next shutdown postgres::

   sudo /etc/init.d/postgresql-8.1 stop

Before we restart, we are going to move the postgres cluster (the files on the
filesystem that are used to store the database information) into /opt/ since
that opt is mapped to a larger partition, and for backup purposes its nice to
have data separate from the main OS partition::

   sudo mv /var/lib/postgresql /opt/
   cd /var/lib/
   sudo ln -s /opt/postgresql .

Now restart postgres::

   sudo /etc/init.d/postgresql-8.3 start

There are three databases that need to be loaded and regularly backed up and restored:

 - gis - All the backdrop gis data e.g. cadastrals, placenames etc
 - sac - The web catalogue database used by the django web catalogue
 - acs - A clone of the legacy ACS catalogue, ported to Postgresql
 -

To load these databases you should create them and then restore them
from a recent backup e.g.::

  createdb gis
  pg_restore gis_postgis_15June2009.dmp |psql gis
  createdb sac
  pg_restore sac_postgis_15June2009.dmp |psql sac
  createdb acs
  pg_restore acs_postgis_15June2009.dmp |psql acs
  ```
  For testing, a sac-test database is used which is a snapshot of the sac database:

  createdb sac-test
  pg_restore  sac_postgis_15June2009.dmp |psql sac-test

After your databases are loaded you should have a db listing like this::

  [elephant:timlinux:~] psql -l
  List of databases
     Name    |  Owner   | Encoding 
  -----------+----------+----------
   gis       | timlinux | UTF8
   postgres  | postgres | UTF8
   sac       | timlinux | UTF8
   sac-test  | timlinux | UTF8
   acs       | timlinux | UTF8
   template0 | postgres | UTF8
   template1 | postgres | UTF8
   (7 rows)

Finally you need to add a rule in the firewall to allow incoming traffic 
on port 5432.

Now go on to test with QGIS to see if you can connect ok.

PostgreSQL 9.1 and GeoDjango 1.2 setup hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Django, prior to version 1.3.2, doesn't support PostgreSQL 9.1 string esaping
settings. See: https://code.djangoproject.com/ticket/16778

As a quick workaround for Django 1.2.x , in ``postgresql.conf`` set
``standard_conforming_strings = off``

Creating readonly user for mapserver access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must do this to allow the mapserver client to connect to the database
securely (ie. ensuring that no sql injection attacks can take place)::

  grant SELECT on vw_usercart to readonly;
  grant select on visit to readonly;
  grant select on search to readonly;

In addition the gis database needs to have permissions set to read only for all
tables for mapserver. Here is a little script I wrote to do that in one go::

  for TABLE in `echo "\dt" | \
    psql -h 196.35.94.197 -U timlinux gis | \
    awk '{print $3}'`
  do  
    echo "grant select on $TABLE to readonly;" >> /tmp/script.sql
  done  
  psql -h 196.35.94.197 -U timlinux gis < /tmp/script.sql

Nightly clone of the sac catalogue to test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For testing we maintain a clone of the sac catalogue. The clone is replaced
nightly. The script to replace the clone is in svn and should be checked out::

  cd /home/timlinux
  svn co https://196.35.94.196/svn/trunk/bash

Now edit the crontab:  ``crontab -e``

And add the clone script to run nightly::

  # Added by Tim for others to see how crontab works
  #*     *     *     *     *  command to be executed
  #-     -     -     -     -
  #|     |     |     |     |
  #|     |     |     |     +----- day of week (0 - 6) (Sunday=0)
  #|     |     |     +------- month (1 - 12)
  #|     |     +--------- day of month (1 - 31)
  #|     +----------- hour (0 - 23)
  #+------------- min (0 - 59)


  # Run a test command every minute to see if crontab is working nicely
  # comment out when done testing
  #*/1 * * * * date >> /tmp/date.txt

  #A script to clone the sac live db nightly into the sac test db
  #Runs at 2:05 am each night
  5 2 * * * /home/timlinux/bash/pg_sac_test_cloner

Source of /home/timlinux/bash/pg_sac_test_cloner (replace XXXXXX with a valid
password)::

  #/bin/bash
  cd /tmp
  export PGPASSWORD=XXXXXXX
  BACKUP=sac_postgis_`date +%d%B%Y`.dmp
  pg_dump -i -Fc -f $BACKUP -x -O sac
  dropdb sac-test
  createdb sac-test
  pg_restore $BACKUP | psql sac-test
  rm $BACKUP
  echo "SAC Test database successfully cloned from $BACKUP" \
     | mail -s "SAC Test database successfully cloned from $BACKUP" \
     tim@linfiniti.com


