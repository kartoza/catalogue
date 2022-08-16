Rolling out updates to the server
=================================

Git Tag
-------

Tag the release::
   
   git tag v2.0.1

Note the tag number for further down!


Opt Backup
----------

Make a backup of the opt directory::
   
   cd /mnt/cataloguestorage/backups/2012/July
   sudo tar cfz opt_SNAPSHOT_PRE_2.0.1.tar.gz /opt/ /etc/apache2

Database backup
---------------

Make a backup of the database (adjust the year/month folder as needed)::

   sudo su - timlinux
   cd /mnt/cataloguestorage/backups/2012/July
   pg_dump -i -U lkleyn -h elephant -Fc -f sac_postgis_SNAPSHOT_PRE_2.0.1.dmp -x -O sac

It is good practive to copy this dump offline and archive it e.g. on a CD.

.. note:: You should do a test restore on a separate system before relying on
   the backup.
   
.. note:: You should run the backup under byobu

Git updates
-----------

Fetch the updates and reload apache::
   
   cd /opt/sac_catalogue/sac_live
   git fetch
   git checkout v2.0.1
   sudo /etc/init.d/apache2 reload

.. note:: You can ignore any message about not being able to reliably
   determine the server name.

Check the server
----------------

Visit the web site and check all that works. If you get a 500 error then you
should look at the apache logs and contact a developer::
   
   tail -100 /var/log/apache2/catalogue.error.log

Run sql updates
---------------

Run any sql updates for the release::

   export PGHOST=elephant
   export PGPASSWORD=xxxxxx
   export PGUSER=lkleyn
   export 
   cd sql/fixes
   run_all.sh


