Configuring the Lion Catalogue server
------------------------------------------

The 'Lion' server provides web mapping services for the SAC Catalogue.

It contains the following key components:

- apache web server
- mapserver cgi with ecw support via custom built gdal
- tilecache
- an instance of the django catalogue software used
- IBM informix client sdk software
- the python informix DB adapter
-

In addition the lion server is connected to two 13TB (effective) Fujitsu Siemens storage arrays.

The Server is an IA 64 processor machine installed with ubuntu server 10.04 LTS. This document
assumes a basic Ubuntu Server LTS install has already been carried out.

Firewall
------------------------------------------

The firewall is configured in the following way::

  sudo apt-get install ufw
  sudo ufw allow 8697
  sudo ufw allow 5432
  sudo ufw allow from 127.0.0.1/32 to 0.0.0.0/0 port 25
  sudo ufw allow from 127.0.0.1/32 to 41.74.158.7/32 port 5432
  sudo ufw allow from 127.0.0.1/32 to 207.97.227.239/32 port 22
  sudo ufw default allow outgoing
  sudo ufw default deny incoming
  sudo ufw status

Where the following ports are allowed:

8697 - ssh, 80 apache, 5432 postgres , 25 outbound mail
22 to 207.97.227.239 is for github access

Package installations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following packages were installed::

  sudo apt-get install bc xterm build-essential lxde rpm mc sun-java6-jre \
  firefox vim ntpdate lxde xinit rpl django python-django subversion \
  utidy python-utidylib python-psycopg2 python-geoip python-django-registration

Setup Fibrecat SX60 Storage arrays
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hardware preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As root / sudo edit the /etc/fstab and disable the storage array at boot. To do
this change this line::

   UUID=3bdda6ae-3195-47b0-955e-278b5ed51da5 /data    ext3       auto,nouser,noexec,nosuid,rw        1 2

to look like this::

   #UUID=3bdda6ae-3195-47b0-955e-278b5ed51da5 /data    ext3       auto,nouser,noexec,nosuid,rw        1 2

The host system was powered off::

sudo /sbin/halt


The fibrecat system was powered off (note that it has redundant power supplies
and both must be powered off).

All drives were then removed and their relative positions and serial numbers
were recorded.

The drives were then removed from their caddies and replacement 1.5TB drives
were inserted in their place.

After all the replacement drives were inserted, the storage array was powered
up again and the system restarted.

We checked that all drives came up properly and no warning lights were displayed.

Configure the storage array in the web admin interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The array is configured using a web control panel at::

   http://196.35.94.141


To login use _____________ for username and _________________ for password.



Next we had to create a virtual disk - removing the old drives destroys any pre-existing vdisks.

- Click on the **manage** link  on the left and then choose **create a vdisk**
- Next choose **Manual Virtual Disk Creation**
- Enter 'sarmesstorage' in the **Enter Virtual Disk Name** box
- For **Select Virtual Disk RAID Level** choose 'Raid 5 - Parity RAID, Parity Distributed'
- Click next to proceed onto disk creation
- Tick all the drives in the enclosure diagram except for the last
- Calculate Formatted Virtual Disk Size of Selected Drives - click this button and verify
  output is something like that shown below here ```For a RAID Level 5, your selected drives
  will approximately yield a 15.00 TByte final virtual disk capacity.```
- For the tickbox **Would you like to add dedicated spare drives for this virtual disk?**, choose Yes
- Click continue
- All the drive bays save the last should now be shown in blue.
- Tick the remaining green bay and then click 'continue' next to the **Add Selected Dedicated Spare
  Drives to "sarmesstorage" and Continue Creating Virtual Disk:** prompt.
-

At this stage you will be shown a report that should look something like this::


  Virtual Disk Name:  sarmesstorage
  RAID Level:     5
  Virtual Disk Size:  201644.88 GBytes
  Drives Chosen:
  Serial Number   WWN     Size (GBytes)   Encl.Slot
  9VS1J496    5000C50011343DE3    1500.30     0.0
  9VS1E8SL    5000C50011229530    1500.30     0.1
  9VS1BWB5    5000C5001115F067    1500.30     0.2
  9VS1BM5F    5000C5001111301C    1500.30     0.3
  9VS1E0WR    5000C500111FC913    1500.30     0.4
  9VS1HZ5M    5000C500113537B4    1500.30     0.5
  9VS1FWXT    5000C500112BCEA2    1500.30     0.6
  9VS1GH9V    5000C500113036EE    1500.30     0.7
  9VS1GZMH    5000C5001130D35D    1500.30     0.8
  9VS1H6A0    5000C50011353891    1500.30     0.9
  9VS1FY6B    5000C500112C210C    1500.30     0.10
  Dedicated Spare Drives Chosen:
  Serial Number   WWN     Size (GBytes)
  9VS1H76L    5000C50011353C6C    1500.30
  Virtual Disk Initialization:    Online

Now we can proceed to set up partitions ('Volumes') on the virtual disk.::

  Configure Volumes for Virtual Disk sarmesstorage
  How Many Volumes    : 1
  Create Volumes of Equal Size?
  Yes
  Expose Volumes to All Hosts?
  No
  Automatically Assign LUNs?
  Disabled
  Would You Like to Name Your Volumes?
  No
  Advanced Virtual Disk Creation Options  Advanced Options - not used

Click 'Create virtual disk' A progress page will appear. Note that the process
will take a loooooong time!

**Note:** It took 3 or 4 days to build the virtual device with 1.5TB disks.

After the virtual disk is built, you need to create a volume mapping.

The volume mapping associates a fibre channel LUN connector to the volume.

In the managment web UI, click: Manage -> volume mapping -> map hosts to volumre.

For the sarmes machine we used the following configuration::

  Current Host-Volume Relationships

  WWN                 Host Name       LUN     Port 0 Access   Port 1 Access
  10000000C96DABE6    Sarmes1_Port0    0       rw               rw
  10000000C961BB34    Sarmes1_Port1    1       rw               rw
  All Other Hosts                      None    none             none

**Note** You probably only need to map one WWN / Host / Lun - we think you only need
to map Sarmes1_port1 to 10000000C961BB34 but you will need to test experimentally to
be sure.

After making these config changes, reboot the sarmes server.

Watch the boot messages or check ``dmesg``

You should see a new device listed like this::

  sd 1:0:0:0: [sdc] Very big device. Trying to use READ CAPACITY(16).
  sd 1:0:0:0: [sdc] 29302441984 512-byte hardware sectors (15002850 MB)
  sd 1:0:0:0: [sdc] Write Protect is off
  sd 1:0:0:0: [sdc] Mode Sense: 93 00 00 08
  sd 1:0:0:0: [sdc] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
  sd 1:0:0:0: [sdc] Very big device. Trying to use READ CAPACITY(16).
  sd 1:0:0:0: [sdc] 29302441984 512-byte hardware sectors (15002850 MB)
  sd 1:0:0:0: [sdc] Write Protect is off
  sd 1:0:0:0: [sdc] Mode Sense: 93 00 00 08
  sd 1:0:0:0: [sdc] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
  sdc: unknown partition table
  sd 1:0:0:0: [sdc] Attached SCSI disk

You can see the drive came up as sdc. It pushes the previous sdc drive down to
sdd. This is not a problem though since the /etc/fstab uses UUIDs to reference partitions.


Next you can verify this using fdisk::

  sudo /sbin/fdisk -l /dev/sdc

  Disk /dev/sdc: 15002.8 GB, 15002850295808 bytes
  255 heads, 63 sectors/track, 1823992 cylinders
  Units = cylinders of 16065 * 512 = 8225280 bytes
  Disk identifier: 0x00000000

  Disk /dev/sdc doesn't contain a valid partition table

By default a DOS partition table is used on new devices and by fdisk. One major
limitation of this is that it does not support partition sizes greater than
2TB, meaning that most of your large disk device will be inaccessible!

There are two ways two resolve this - using a raw xfs partition (as we have
done on SARMES), or using the GPT partition table scheme as we have done on
LION).

Creating a large filesystem using GPT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For newer systems we want to use ext4 on a large (non raw) filesystem The
kernel must have been compiled with GPT support (it is by default under UBUNTU
Jaunty Server Edition >= 9.04). In addition, we need to use **parted** (the
command line version of gparted) to format the disk and create the GPT
partition table.

In Linux parlance, determining the partition table type is called 'setting the
disk label'. In the console transcripts that follow we will set the disk label
to GPT, create a large single partition and then format and mount the drive.
Once this has been completed, we will use a similar procedure as described
above to add an fstab entry so that the volume is mounted at boot time.


This is the procedure I used to create a large ext4 partition using parted::

  (parted) unit s
  (parted) print
  Model: FSC FibreCAT_SX1 (scsi)
  Disk /dev/sdc: 29302441984s
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt

  Number  Start  End  Size  File system  Name  Flags

  (parted) mkpart
  Partition name?  []? cataloguestorage2
  File system type?  [ext2]? ext4
  Start? 34
  End? 29302441950
  Warning: The resulting partition is not properly aligned for best performance.
  Ignore/Cancel? cancel
  (parted) mkpart cataloguestorage2 ext4 1 -1
  Warning: You requested a partition from 1s to 29302441983s.
  The closest location we can manage is 34s to 29302441950s.
  Is this still acceptable to you?
  Yes/No? yes
  Warning: The resulting partition is not properly aligned for best performance.
  Ignore/Cancel? Ignore
  (parted) p
  Model: FSC FibreCAT_SX1 (scsi)
  Disk /dev/sdc: 29302441984s
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt

  Number  Start  End           Size          File system  Name               Flags
   1      34s    29302441950s  29302441917s               cataloguestorage2

The process sets the drive units to sectors, then creates a new partition
leaving 34sectors at the start of the drive.

Now exit parted and create the filesystem::

  sudo mkfs.ext4 /dev/sdc1

Note it will take a little while to process. Finally add a new mount point for
the partition and mount it.::

  mkdir /mnt/cataloguestorage2

Add an entry to /etc/fstab::

  /dev/sdc1 /mnt/cataloguestorage2            ext4    relatime,errors=remount-ro        0       2



Informix Client Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When following the Informix install procedure, do it as root locally on
the server since I had problems trying to run the sdk setup tool remotely over
an ssh -X connection.

For specific notes on how to set up the client see the informix specific notes
(003-3-informix_access.t2t).

Nightly database sync
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We should sync the ACS data to our own catalogue database nightly. When all
the prerequisites are installed on the Lion server, the updateInformix.sh script
can be used to do this on an ad hoc basis. Automating the process requires
creation of a cron job::

  crontab -e


Now add the following (adjusing paths if needed)::

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

  # Run informix stats update nightly to keep responsiveness good
  # Job will run 5 min after midnight
  5 0 * * * /home/timlinux/dev/python/sac_catalogue/updateInformix.sh

Nightly database backups from elephant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For prudence sake, a nightly dump is made of the databases on ELEPHANT onto
the LION server ``crontab -e``::

  # Job will run 2:05 am each day
  5 2 * * * /home/timlinux/bin/pgbackups


The second job described above takes a backup of the gis and catalogue
databases on a nightly basis. The pgbackups script looks like this::

  #/bin/bash

  cd /mnt/cataloguestorage/backups/
  MONTH=$(date +%B)
  YEAR=$(date +%Y)
  mkdir -p $YEAR/$MONTH
  cd $YEAR/$MONTH
  tar cfz opt_`date +%d%B%Y`.tar.gz /opt/ /etc/apache
  export PGPASSWORD=pumpkin
  pg_dump -i -U timlinux -h elephant -Fc -f gis_postgis_`date +%d%B%Y`.dmp -x -O gis
  pg_dump -i -U timlinux -h elephant -Fc -f sac_postgis_`date +%d%B%Y`.dmp -x -O sac
  pg_dump -i -U timlinux -h elephant -Fc -f acs_postgis_`date +%d%B%Y`.dmp -x -O acs
  psql -h elephant -c "vacuum analyze;" sac
  psql -h elephant -c "vacuum analyze;" sac_test

To restore you do::

  createdb sac
  createdb gis
  pg_restore sac_[filename].dmp | psql sac
  pg_restore gis_[filename].dmp | psql gis
  pg_restore acs_[filename].dmp | psql acs

GDAL and Mapserver Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please see the webmapping chapter (600-webmapping.t2t) for notes on the setup process for GDAL

**Note:** When installing gdal from source and you want the python bindings installed into your
python virtual env, make sure to activate the virtual environment begore building gdal so that
its bindings are placed in the v.env site packages dir.

Apache setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are specific notes for the catalogue application in the developer guide. The apache
configuration for default (/etc/apache2/sites-available/default) is as listed below.::
  NameVirtualHost *
  <VirtualHost *>
    ServerAdmin tim@linfiniti.com
    ServerName maps.sansa.org.za
    DocumentRoot /var/www/
    <Directory /var/www/>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride None
      Order allow,deny
      allow from all
    </Directory>

    Alias /ss1 /mnt/cataloguestorage/sumbandilasat/SS1
    <Directory /mnt/cataloguestorage/sumbandilasat/SS1>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride None
      Order allow,deny
      allow from all
    </Directory>

    Alias /shade /mnt/cataloguestorage/data/world/aster_dem/final
    <Directory /mnt/cataloguestorage/data/world/aster_dem/final>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride None
      Order allow,deny
      allow from all
    </Directory>

    # Options for fastcgi support:
    # FastCgiConfig -appConnTimeout 60 -idle-timeout 60 -init-start-delay 1 -minProcesses 2 -maxClassProcesses 20 -startDelay 5

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    <Directory "/usr/lib/cgi-bin">
      #Next two lines added by Tim for PyWPS
      SetEnv PYWPS_CFG /etc/pywps.cfg
      SetEnv PYWPS_PROCESSES /opt/wps-processes/sac
      PythonPath "['/opt/','/opt/wps-processes/sac'] + sys.path"
      AllowOverride None
      #Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
      #changed from above for pywps
      Options +ExecCGI -MultiViews +FollowSymLinks
      Order allow,deny
      Allow from all
    </Directory>

    #Alias and dir below added for pywps
    Alias /wps_outputs/ "/tmp/wps_outputs"
    <Directory "/tmp/wps_outputs/">
        Options Indexes MultiViews FollowSymLinks
        AllowOverride None
    </Directory>

    <Location "/sarmes2">
      AuthType Basic
      AuthName "sac"
      AuthUserFile /etc/apache2/dims.passwd
      Require valid-user
    </Location>


    ErrorLog /var/log/apache2/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog /var/log/apache2/access.log combined
    ServerSignature On

    # For munin server monitoring
    Alias /munin/ "/var/www/munin/"


    # Reverse proxy to the ordering service on dims
    ProxyRequests Off

    <Proxy *>
    Order deny,allow
    Allow from all
    </Proxy>
    # This will no longer work since entry into the vpn
    # Was really only for testing anyway.
    #ProxyPass /os4eo http://196.35.94.248:8080/hma/ordering
    #ProxyPassReverse /os4eo http://196.35.94.248:8080/hma/ordering



  </VirtualHost>

This creates various share points through the file system. You should
evaluate the file and check that each of the share points listed is
indeed present and with the appropriate permissions in the file system.


Proxying Ordering Service Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ordering service on jackal is not a publicly accessible server so we
proxy access to it via lion.

```
sudo apt-get install libapache2-mod-proxy-html
sudo a2enmod proxy_http proxy_html headers
```

Now add proxy config to 000-default (as listed in the apache section above).

*Note:* No longer valid since moving into the vpn. Also was only needed for testing::

  # Reverse proxy to the ordering service on dims
  ProxyRequests Off

  <Proxy *>
  Order deny,allow
  Allow from all
  </Proxy>

  ProxyPass /os4eo http://196.35.94.248:8080/hma/ordering
  ProxyPassReverse /os4eo http://196.35.94.248:8080/hma/ordering



Fibrecat storage arrays config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Catalogue Storage 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IP Address: 192.168.1.142

Rack Position: **Upper** device as you look at the rack

A  WWN: 207000c0ff03a2c3 196.35.94.142 Catalogue Storage::

  RAID Controller B       Yes     Failed  System Detected Failure         862821-0743MV00AK       Down
  "cataloguestorage" Volume Information
  Number  Name                    LUN     Size (Mbytes)
  1       cataloguestorage1       0       15002850


  Status  Size (GB)       Manufacturer Model:Revision     Node WWN Serial Number  Chan:LoopID Port0 Port1         Enclosure
  Up      1500.30GB       ATA             ST31500341AS    WWN:5000c5001120e443    SN:9VS1CC29     0:11   ----


Catalogue Storage 2 (old Sarmes Storage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IP Address: 192.168.1.141


A  WWN: 207000c0ff0a66c8 196.35.94.141 Sarmes Storage

Rack Position: **Lower** device as you look at the rack



Lion configuration as fibrecat client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the configuration::

  timlinux@lion:~$ dmesg | grep scsi
  [    1.505180] scsi0 : ata_piix
  [    1.505252] scsi1 : ata_piix
  [    1.506339] scsi2 : ata_piix
  [    1.506396] scsi3 : ata_piix
  [    1.809264] scsi 2:0:0:0: Direct-Access     ATA      ST3750640NS      n/a  PQ: 0 ANSI: 5
  [    1.809395] sd 2:0:0:0: Attached scsi generic sg0 type 0
  [    1.813674] scsi 3:0:0:0: Direct-Access     ATA      ST3750640NS      n/a  PQ: 0 ANSI: 5
  [    1.813810] sd 3:0:0:0: Attached scsi generic sg1 type 0
  [    2.271356] scsi4 : qla2xxx
  [    2.630121] scsi5 : qla2xxx
  [    3.602342] scsi 4:0:0:0: Enclosure         FSC      FibreCAT_SX1     J200 PQ: 0 ANSI: 4
  [    3.603234] scsi 4:0:1:0: Enclosure         FSC      FibreCAT_SX1     J200 PQ: 0 ANSI: 4
  [    3.610832] scsi 4:0:0:0: Attached scsi generic sg2 type 13
  [    3.610957] scsi 4:0:1:0: Attached scsi generic sg3 type 13
  [    3.962310] scsi 5:0:0:0: Direct-Access     FSC      FibreCAT_SX1     J110 PQ: 0 ANSI: 3
  [    3.963175] scsi 5:0:1:0: Enclosure         FSC      FibreCAT_SX1     J110 PQ: 0 ANSI: 3
  [    3.972099] sd 5:0:0:0: Attached scsi generic sg4 type 0
  [    3.972210] ses 5:0:1:0: Attached scsi generic sg5 type 13


File System Layout on the catalogue server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following are the key areas of the file system you should be aware of:

Opt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the layout::

  /opt
  +-- sac_catalogue
  |   +-- python
  |   +-- sac_live
  |   +-- sac_test
  +-- webmapping
      +-- config
      +-- data -> /mnt/cataloguestorage/data/
      +-- fonts
      +-- mapfiles
      +-- scripts
      +-- symbols
      +-- templates

/usr/local
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the recommended place in which user compile applications should be
installed to. Our installations of gdal, mapserver etc have been placed in this
part of the filesystem when installed.

/mnt/cataloguestorage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the first of two ~13TB storage arrays connected to the server. In this
storage system, all of the thumbnailas, online remote sensing dataset, backups
and data that is being processed are stored.::

  /mnt/cataloguestorage
  +-- backups
  |   +-- 2010
  |   +-- 2011
  +-- data
  |   +-- africa
  |   +-- thumbs
  |   +-- world
  |   +-- za
  +-- imagery_master_copy
  |   +-- C2B
  |   +-- S-C
  |   +-- ZA2
  +-- imagery_processing
  |   +-- cbers
  |   +-- sacc
  |   +-- sumbandilasat
  +-- mapproxy
  |   +-- etc
  |   +-- tmp
  |   +-- var
  +-- thumbnail_processing
  |   +-- georeferenced_segments_out
  |   +-- georeferenced_thumbs_out
  |   +-- segments_out
  |   +-- thumb_blobs
  |   +-- to_erase
  +-- thumbnails_master_copy
  |   +-- C2B
  |   +-- cache
  |   +-- E1
  |   +-- E2
  |   +-- L2
  |   +-- L3
  |   +-- L4
  |   +-- L5
  |   +-- L7
  |   +-- N11
  |   +-- N12
  |   +-- N14
  |   +-- N15
  |   +-- N16
  |   +-- N17
  |   +-- N9
  |   +-- S1
  |   +-- S2
  |   +-- S4
  |   +-- S5
  |   +-- SACC
  |   +-- S-C
  |   +-- ZA2
  +-- tilecache
      +-- README
      +-- spot5mosaic10m2007
      +-- spot5mosaic10m2007_4326
      +-- spot5mosaic10m2008
      +-- spot5mosaic10m2008_4326
      +-- spot5mosaic10m2009
      +-- spot5mosaic10m2098_4326
      +-- spot5mosaic2m2007
      +-- spot5mosaic2m2008
      +-- spot5mosaic2m2009
      +-- za_vector
