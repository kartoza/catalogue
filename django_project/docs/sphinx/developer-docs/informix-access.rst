Informix SPOT Catalogue Notes
------------------------------------------

Accessing the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
ssh 196.35.94.210 -l informix
```

Interactive database access:

```
dbaccess
```

Command line batch processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add some sql commands to a text file:

```
vim /tmp/tim.sql
```

Some commands:

```
select geo_time_info from ers_view;
```

Save and run, redirecting output to another text file:

```
dbaccess catalogue < /tmp/tim.sql >> /tmp/tim.out
```

Command line processing using echo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Handy for quickly running once off commands of from bash
scripts.

```
echo "select * from t_file_types" | dbaccess catalogue
```

Changing geotype to wkt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For batch export to the django catalogue the geometries
need to be exported as wkt (well known text) which is not
the type used internally for the spot catalogue.

```
echo "update GeoParam set value = 0 where id =3;" | dbaccess catalogue
```

Reverting geotype to informix format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To set geometry output back informix representation and restoring
normal catalogue functioning do:

```
echo "update GeoParam set value = 4 where id =3;" | dbaccess catalogue
```

Connecting to the database using python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Download the InformixDB driver for python from:

```
http://sourceforge.net/project/showfiles.php?group_id=136134
```

And the Informix client sdk from:

```
http://www14.software.ibm.com/webapp/download/preconfig.jsp?id=2007-04-19+14%3A08%3A41.173257R&S_TACT=104CBW71&S_CMP==
```

If the above link doesnt work for you (it seems to contain a session id), go to the

```
http://www14.software.ibm.com
```

website and search for

```
3.50.UC4
```

using the search box near the top right of the page. Downloading requires an
IBM id etc. which you can sign up for if you dont have one.

**Note:** You will need to get the appropriate download for your processor
type. For Lion, which is running ubuntu server x86_64, I downloaded the sdb
bundle called:

```
IBM Informix Client SDK V3.50.FC4 for Linux (x86) RHEL 4, 64bit
clientsdk.3.50.FC4DE.LINUX.tar  (72MB)
```

**Note 2:** Even though it says Red Hat Enterprise Editition (RHEL) you can use
it on ubuntu servers too.
After you have downloaded the client sdk do the following to install (below is a log of my install process).

```
sudo adduser informix
Adding user `informix' ...
Adding new group `informix' (1003) ...
Adding new user `informix' (1003) with group `informix' ...
Creating home directory `/home/informix' ...
Copying files from `/etc/skel' ...
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
Changing the user information for informix
Enter the new value, or press ENTER for the default
	Full Name []: Informix
	Room Number []:
	Work Phone []:
	Home Phone []:
	Other []:
Is the information correct? [Y/n] Y
[linfiniti:timlinux:DownloadDirector] sudo ./installclientsdk








         Initializing InstallShield Wizard........
          Launching InstallShield Wizard........


-------------------------------------------------------------------------------
Welcome to the InstallShield Wizard for IBM Informix Client-SDK Version 3.50

The InstallShield Wizard will install IBM Informix Client-SDK Version 3.50 on
your computer.
To continue, choose Next.

IBM Informix Client-SDK Version 3.50
IBM Corporation
http://www.ibm.com


Press 1 for Next, 3 to Cancel or 4 to Redisplay [1] 1

-------------------------------------------------------------------------------
     International License Agreement for Non-Warranted Programs

     Part 1 - General Terms

     BY DOWNLOADING, INSTALLING, COPYING, ACCESSING, OR USING THE PROGRAM
     YOU AGREE TO THE TERMS OF THIS AGREEMENT. IF YOU ARE ACCEPTING THESE
      TERMS ON BEHALF OF ANOTHER PERSON OR A COMPANY OR OTHER LEGAL
      ENTITY, YOU REPRESENT AND WARRANT THAT YOU HAVE FULL AUTHORITY TO
      BIND THAT PERSON, COMPANY, OR LEGAL ENTITY TO THESE TERMS. IF YOU DO
      NOT AGREE TO THESE TERMS,



- DO NOT DOWNLOAD, INSTALL, COPY, ACCESS, OR USE THE PROGRAM; AND



- PROMPTLY RETURN THE PROGRAM AND PROOF OF ENTITLEMENT TO THE PARTY

Press Enter to continue viewing the license agreement, or, Enter "1" to accept
the agreement, "2" to decline it or "99" to go back to the previous screen, "3"
 Print.

1

Press 1 for Next, 2 for Previous, 3 to Cancel or 4 to Redisplay [1] 1

-------------------------------------------------------------------------------
IBM Informix Client-SDK Version 3.50 Install Location

Please specify a directory or press Enter to accept the default directory.

Directory Name: [/opt/IBM/informix] /usr/informix

Press 1 for Next, 2 for Previous, 3 to Cancel or 4 to Redisplay [1] 1

-------------------------------------------------------------------------------
Choose the setup type that best suits your needs.

[X] 1 - Typical
        The program will be installed with the suggested configuration.
        Recommended for most users.

[ ] 2 - Custom
        The program will be installed with the features you choose.
        Recommended for advanced users.

To select an item enter its number, or 0 when you are finished: [0]


Press 1 for Next, 2 for Previous, 3 to Cancel or 4 to Redisplay [1] 1

-------------------------------------------------------------------------------
IBM Informix Client-SDK Version 3.50 will be installed in the following
location:

/usr/informix

with the following features:

Client
Messages
Global Language Support (GLS)

for a total size:

 91.8 MB

Press 1 for Next, 2 for Previous, 3 to Cancel or 4 to Redisplay [1] 1

Installing IBM Informix Client-SDK Version 3.50. Please wait...


|-----------|-----------|-----------|------------|
0%         25%         50%         75%        100%
||||||||||||||||||||||||||||||||||||||||||||||||||

Creating uninstaller...
Performing GSKit installation for Linux ...


Branding Files ...
Installing directory .
Installing directory etc
Installing directory bin
Installing directory lib
Installing directory lib/client
Installing directory lib/client/csm
Installing directory lib/esql
Installing directory lib/dmi
Installing directory lib/c++
Installing directory lib/cli
Installing directory release
Installing directory release/en_us
Installing directory release/en_us/0333
Installing directory incl
Installing directory incl/esql
Installing directory incl/dmi
Installing directory incl/c++
Installing directory incl/cli
Installing directory demo
Installing directory demo/esqlc
Installing directory demo/c++
Installing directory demo/cli
Installing directory doc
Installing directory doc/gls_api
Installing directory doc/gls_api/en_us
Installing directory doc/gls_api/en_us/0333
Installing directory tmp
Installing directory gsk
Installing directory gsk/client
Installing directory gskit
Installing directory gsk
Installing directory gsk/client

IBM Informix Product:       IBM INFORMIX-Client SDK
Installation Directory: /usr/informix

Performing root portion of installation of IBM INFORMIX-Client SDK...


Installation of IBM INFORMIX-Client SDK complete.

Installing directory etc
Installing directory gls
Installing directory gls/cm3
Installing directory gls/cv9
Installing directory gls/dll
Installing directory gls/etc
Installing directory gls/lc11
Installing directory gls/lc11/cs_cz
Installing directory gls/lc11/da_dk
Installing directory gls/lc11/de_at
Installing directory gls/lc11/de_ch
Installing directory gls/lc11/de_de
Installing directory gls/lc11/en_au
Installing directory gls/lc11/en_gb
Installing directory gls/lc11/en_us
Installing directory gls/lc11/es_es
Installing directory gls/lc11/fi_fi
Installing directory gls/lc11/fr_be
Installing directory gls/lc11/fr_ca
Installing directory gls/lc11/fr_ch
Installing directory gls/lc11/fr_fr
Installing directory gls/lc11/is_is
Installing directory gls/lc11/it_it
Installing directory gls/lc11/ja_jp
Installing directory gls/lc11/ko_kr
Installing directory gls/lc11/nl_be
Installing directory gls/lc11/nl_nl
Installing directory gls/lc11/no_no
Installing directory gls/lc11/os
Installing directory gls/lc11/pl_pl
Installing directory gls/lc11/pt_br
Installing directory gls/lc11/pt_pt
Installing directory gls/lc11/ru_ru
Installing directory gls/lc11/sk_sk
Installing directory gls/lc11/sv_se
Installing directory gls/lc11/th_th
Installing directory gls/lc11/zh_cn
Installing directory gls/lc11/zh_tw

IBM Informix Product:       Gls
Installation Directory: /usr/informix

Performing root portion of installation of Gls...


Installation of Gls complete.

Installing directory etc
Installing directory msg
Installing directory msg/en_us
Installing directory msg/en_us/0333

IBM Informix Product:       messages
Installation Directory: /usr/informix

Performing root portion of installation of messages...


Installation of messages complete.


-------------------------------------------------------------------------------
The InstallShield Wizard has successfully installed IBM Informix Client-SDK
Version 3.50. Choose Finish to exit the wizard.

Press 3 to Finish or 4 to Redisplay [3]
```

Note that trying to install it to another directory other than /usr/informix will
cause the db adapter build to fail (and various other issues). So dont accept the
default of /opt/IBM/informix and rather use /usr/informix


Now build the python informix db adapter:

```
cd /tmp/InformixDB-2.5
python setup.py build_ext
sudo python setup.py install
```


Now ensure the informix libs are in your lib search path:

```
sudo vim /etc/ld.so.conf
```

And add the following line:

```
/usr/informix/lib/
/usr/informix/lib/esql
```

Then do

```
sudo ldconfig
```

Making a simple python test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First you need to add a line to informix's sqlhosts file:

```
sudo vim /usr/informix/etc/sqlhosts
```

And add a line that looks like this:

```
#catalog2 added by Tim
#name, protocol, ip, port
catalog2        onsoctcp        196.35.94.210  1537
```

Next you need to export the INFORMIXSERVER environment var:

```
export INFORMIXSERVER=catalog2
```


I found out that it is running on port 1537 by consulting the /etc/services file on the informix server.
Now lets try our test connection.This little script will make a quick test connection so you can see
if its working:

```
#!/usr/bin/python

import sys
import informixdb  # import the InformixDB module

# ------------------------------------
# open connection to database 'stores'
# ------------------------------------
conn = informixdb.connect('catalogue@catalog2', user='informix', password='')

# ----------------------------------
# allocate cursor and execute select
# ----------------------------------
cursor1 = conn.cursor(rowformat = informixdb.ROW_AS_DICT)
cursor1.execute('select * from t_file_types')

for row in cursor1:

  # -------------------------------------------
  # delete row if column 'code' begins with 'C'
  # -------------------------------------------
  print "%s %s" % (row['id'], row['file_type_name'])
# ---------------------------------------
# commit transaction and close connection
# ---------------------------------------
conn.close()

sys.exit(0);

```





Note that the documentation for the python InformixDB module is available here:

```
http://informixdb.sourceforge.net/manual.html
```

And the documentation for the Informix SQL implementation is here:

```
http://publib.boulder.ibm.com/infocenter/idshelp/v10
```

WKT representation of GeoObjects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Informix uses its own representation of geometry objects. There are two extensions
for informix that deal with spatial data : Geodetic and Spatial. It seems we have
only geodetic extension at SAC and thus can't use ST_foo functions to work with
geometry fields. For Geodetic we need to alter a value in the GeoParam table
in order to change what formats are output / input. From the manual:


```
Converting Geodetic to/from OpenGIS Formats

Geodetic does not use functions to convert data to a specific format.

Instead, the GeoParam metadata table manages the data format for transmitting
data between client and server. If the "data format" parameter is set to "OGC",
then binary i/o is in WKB format and text i/o is in WKT format. (For specific
details, see Chapter 7 in the Informix Geodetic DataBlade Module User's Guide).
```



You can
override the representation type that should be returned so that you
get e.g. WKT  back instead. Consider this example:

```
-- set output format to 3
update GeoParam set value = 4 where id =3;
-- show what the format is set to now
select * from GeoParam where id = 3;
-- display a simple polygon
select first 1 geo_time_info from t_localization;
-- revert it to informix representation
update GeoParam set value = 0 where id =3;
-- display the polygon back in native informix representation
select first 1 geo_time_info from t_localization;
--verify that the format is reverted correctly
select * from GeoParam where id = 3;
```

Which produces output like this:

```
id       3
name     data format
value    4
remarks  This parameter controls the external text & binary format of GeoObject
         s.  It is not documented in the 3.0 version of the user's guide.  See
         release notes for more info.



geo_time_info  POLYGON((28.73 -15.35, 28.969999 -13.79, 27.34 -13.55, 27.1 -15.
                        11, 28.73 -15.35))



geo_time_info  GeoPolygon((((-15.35,28.73),(-13.79,28.969999),(-13.55,27.34),(-
                         15.11,27.1))),ANY,(1987-04-26 07:34:45.639,1987-04-26 07:34:45.6
                         39))



id       3
name     data format
value    0
remarks  This parameter controls the external text & binary format of GeoObject
         s.  It is not documented in the 3.0 version of the user's guide.  See
         release notes for more info.

```

When things go wrong on the informix server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

==== Record Lock Issues ====
If the client does not cleanly disconnect it can leave records locked. You may
see a message like this from dbaccess when trying to do an interactive query:

```
244: Could not do a physical-order read to fetch next row.
107: ISAM error:  record is locked.
```

There are probably solutions that are better than this, but the most robust way
of dealing with the issue is to restart the informix database:

```
ssh informix@informix
cd /home/informix/bin
onmode -k
```

You will then get prompted like this:

```
This will take Informix Dynamic Server 2000 OFF-LINE -
Do you wish to continue (y/n)? y

There are 1 user threads that will be killed.
Do you wish to continue (y/n)? y
```

Afterwards, you can bring up the database like this:

```
oninit
```

The record locks should have been cleared at this point.


==== DBAccess Unresponsive ====


Collect diagnostics:

[101] catalog2:/home/informix> onstat -V
Informix Dynamic Server 2000 Version 9.21.UC4 Software Serial Number AAD#J130440

[101] catalog2:/home/informix> onstat -a

Sent above and online.log to "Sergio Folco" <sergio.folco.GW-EMI@acsys.it> for diagnostics.

I have stored the logs for issues dating from 7 Jan 2009 in svn under informix_errors/


Following response from ACS, I added a cronjob to do a nightly analyse on the database:

```
ssh informix@informix
crontab -l
[101] catalog2:/home/informix> crontab -l
no crontab for informix
```

So now we make a little bash script:

```
#!/bin/bash

# A simple bash script to  be invoked by CRON on a nightly basis
# To enable add to your crontab like so:
#
# -------------------------------------------------------------
#
# Run informix stats update nightly to keep responsiveness good
# Job will run 5 min after midnight
# 5 0 * * * /home/informix/nightly_cron.sh
#
# -------------------------------------------------------------
#
# Actual script follows:
#
# Tim Sutton, May 2009
#

# Update the db stats on a nightly basis:

date >> /tmp/informix_stats_update_cron_log.txt
echo "Nightly stats update running" >> /tmp/informix_stats_update_cron_log.txt
echo "update statistics high;" | dbaccess catalogue >> /tmp/informix_stats_update_cron_log.txt
```




And then set up a nightly cronjob to run it:

```
crontab -e
```

Now add this:


```
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
5 0 * * * /home/informix/nightly_cron.sh
```

File System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
root@informix's password:
Last login: Tue Sep  9 12:57:53 2008 from :0
[root@catalog2 /root]# mount
/dev/sda6 on / type ext2 (rw)
none on /proc type proc (rw)
usbdevfs on /proc/bus/usb type usbdevfs (rw)
/dev/sda2 on /boot type ext2 (rw)
/dev/sda10 on /home type ext2 (rw)
/dev/sda8 on /tmp type ext2 (rw)
/dev/sda5 on /usr type ext2 (rw)
/dev/sda9 on /var type ext2 (rw)
none on /dev/pts type devpts (rw,gid=5,mode=620)
/dev/sdb1 on /mnt/disk1 type ext2 (rw)
/dev/sdc1 on /mnt/disk2 type ext2 (rw)
automount(pid458) on /misc type autofs (rw,fd=5,pgrp=458,minproto=2,maxproto=3)
```

Schema dump of informix databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Its useful to be able to see the schema of databases so you can understand how
it was put together. The following command will dump the catalogue2 (SAC
Production database) schema to a text file. **Note:** No data is dumped in this
process.

```
dbschema -t all -d catalogue catalogue_schema.sql
```

Listing system and user functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To see what functions are installed in the database do:

```
select procname from sysprocedures;
```

To see full details of a function:

```
select * from sysprocedures where procname="lotofile";
```

Problems running functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you try to run a function that you know exists, but you get an error message
like this:

```
_informixdb.DatabaseError: SQLCODE -674 in PREPARE:
IX000: Routine (lotofile) can not be resolved.
```

It probably means you passed the incorrect number or type of parameters to the
function.
