

%---------above lines left blank intentionally
== Lion File Drop ==

Lion (the catalogue server) should be isolated in the network from other SANSA
servers and infrastructure (with the exception of the elephant database
server). In addition the server has been locked down as much as possible and we
do not wish to run services such as ftp on it. Thus in order to make files
available to the catalogue server for processing, data should be **pushed**
to the server and not **pulled** from other servers on the network. This will
allow the system to be configured without making holes through the firewall
to facilititate file transfers off internal servers.

[img/network-dmz.png]




To achieve a drop directory capability, the installation on the catalogue
server provides rsync (remote synchronisation) access over ssh (secure shell)
using rssh (restricted shell).

The following diagram illustrates the logic flow for the filedrop.

[img/filedrop.png]

=== Setup rssh ===

```
sudo apt-get install rssh
```

=== Creating a filedrop user ===

Next we make a user with a rssh (restricted shell) that can only use scp and rsync.

```
sudo useradd -m -d /mnt/cataloguestorage2/filedrop -s /usr/bin/rssh filedrop
sudo su - filedrop -s /bin/bash
ssh-keygen -N ''
```

The -N option should suppress prompting for a passphrase - no passphrase is
entered so that keybased authentication can be used during non-interactive
sessions (such as from a cron job) to transfer files.

After this, a public and private keypair exist in
''/mnt/cataloguestorage2/filedrop/.ssh''. The private key should be copied to
any server that will be synchronising files into the filedrop directory. This
is explained in more detail further on in this document. 


Now exit the filedrop user's shell:

```
exit
```

=== Ssh configuration ===

Next sshd has to be configured to allow connections for the filedrop user. To
do this, edit ''/etc/ssh/sshd_config'' and add the filedrop user to the
AllowUsers clause:

```
AllowUsers timlinux cstephens modisdbc0 filedrop
```

And then restart sshd:

```
sudo /etc/init.d/ssh restart
```

=== Authorized Keys for filedrop ===

Next we configure the filedrop user's authorised keys file so that key based
connections from a specific host can be made.

**Note:** the 'specific host' part above is an additional security measure.
This step needs to be repeated for each client that may want to deposit files
into the filedrop.

```
sudo su - filedrop -s /bin/bash
cd .ssh/
cp id_rsa.pub authorized_keys
chmod 600 authorized_keys 
```

Now edit authorized_keys and prepend the server ip address that will be copying
files over. We will use cheetah for the purposes of this document.

```
#
# Restrict access to cheetah and orasac1. Lines wrapped here for convenience in this document
#
from="cheetah,orasac1",no-port-forwarding,no-pty ssh-rsa
AAAAB3NzaC1yc2EAAAABIwAAAQEA0iDxnisywfqqzNN2CUN2xJBIOhyvoAA9uqHDagN620UFH4A4Egdg
5am0CsDT8jm1VO/Y2ZCuyKNCmkRCnhPv4IeblsHFc2ekfZsZpSPYYAupUo43POhfwcAPUvdoec1fuBJd
o+Y/zNBz8T0mAr3Mbc0zf5pLgdA3VE44TauCEt6KJ0OAzqzlYEI1tmKFZ4VacgeDhEv9246HbmpEiAoW
waMlkiIWKhV1j3w1OXiMp20pSbenGnw/2dN3avWFte3Wm4DFtnAR9MwppQ+4oyGVsG6rWgmIRVfamX1p
4FeWqnOPYfe9dCIk298GgiIHpmsGHf6Ce7uKYG F7aYW0enIFEw== filedrop@lion
```

**Note:** You can allow additional hosts by comma separating them e.g.
''from="*.foo.co.za,!bar.co.za"''. The wildcard means all hosts from that
prefix. The ! means deny access to that host.

Now exit the filedrop shell again:

```
exit
```

=== Configuring rssh ===

The final thing to do on the server side is to configure rssh.

```
sudo vim /etc/rssh.conf
```

Simply uncomment the rsync and scp lines:

```
allowscp
#allowsftp
#allowcvs
#allowrdist
allowrsync
#allowsvnserve

```

There is no need to restart ssh, the changes should take effect immediately on
saving the file.

=== Testing from a client ===

To test from the client (cheetah in this case), you need to copy the
**private** key over to that server

```
sudo su - filedrop -s /bin/bash
cd .ssh
scp id_rsa timlinux@cheetah:/tmp/
```

Immediately, log in to cheetah and move the key into root's home:

```
ssh cheetah
sudo su -
cd .ssh
mv /tmp/id_rsa .ssh/filedrop_private_key
```

Now do a simple test to see if you can copy over a file to the remote system:

```
touch /tmp/test222
scp -i ~/.ssh/filedrop_private_key -P 8697 /tmp/test222 filedrop@196.35.94.243:/tmp/
```

Note the -i parameter explicitly defines which private key to use for key based
authentication.

The file should successfully copy over. As an additional test, verify that no
ssh access is allowed for the filedrop user on lion:

```
cheetah:~ # ssh filedrop@196.35.94.243 -p 8697 -i .ssh/filedrop_private_key 
                    |\_
Daniel C. Au     -' | `.
               /7      `-._
              /            `-._________\|\||___
              \-'_                    -- |||||/,`-.
                -- `-.              /7   ||||||/-  |.
                     |\            /    ||||||||/`   \
                     | \  \______..\-' ||||||||||______________
                     |  \  \         -/||||||||\               `-.
                     |  |\  \         /||||||\            /      \
                     _/  / _|  ) _______///|||\|      ______\      |\_
                     /,__/ /,__/ /,__________/ `-..___/,_____________-\`=_ __--.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ``---'

This account is restricted by rssh.
Allowed commands: scp rsync 
If you believe this is in error, please contact your system administrator.
Connection to 196.35.94.243 closed.

```

**Note:** for additional security, the filedrop directory could be placed in a
chroot environment see for example [this article
http://www.cyberciti.biz/tips/howto-linux-unix-rssh-chroot-jail-setup.html].
However this was not implemented in this work package and will remain an
activity for a future work package.


=== Streamlining ssh parameters on client ===

As you can see from above, there are a number of options that need to be passed
when making the connection:

|| Flag | Meaning |
| -p 8697 | Connect on the 8697 port (non standard for security reasons) |
| -i .ssh/filedrop_private_key | Use a specified private key |
| 196.35.94.243 | The ip address of the host to connect to |
| filedrop@ | The user to connect as |

We can automate these items by placing the following into the ~/.ssh/config of
the root user on the client system.

```
 Host lion
  User filedrop
  Port 8697
  HostName 196.35.94.243
  FallBackToRsh no
  Compression yes
  CompressionLevel 9
  IdentityFile /root/.ssh/filedrop_private_key
```

With the above config file, the syntax for copying a file over is much more streamlined:

```
scp /tmp/test222 lion:/tmp/
```

=== Synchronising with a cron job ===

The DIMS product library extraction places products in
''/cxfs/eods/deliveries/'' when they are ready. We can thus synchronise these
over to the catalogue server as they are created and ingest their metadata.



```
echo "The filedrop directory was created by Tim for " > filedrop-README.txt
echo "synchronising files over to lion:/mnt/cataloguestorage2/filedrop" >> filedrop-README.txt
echo "Take a look at filedrop user's crontab for details on synchronisation frequency." >> filedrop-README.txt
cd filedrop
touch test
rsync -ave ssh . lion:/mnt/cataloguestorage2/filedrop/
```

Assuming that works correctly, we create a simple script that we will run from cron that 
performs a sync every 5 minutes (script saved as ''/usr/local/bin/sac/sync_dims_deliveries'').


**Note:** The second part of this script is commented out. If enabled it will
flush any files that are older then 7 days. However I do **not** recommend
running that as root, so it is disabled.

```
#!/bin/bash
# This should be run in a cron job at 5 min intervals (or similar) by root to 
# push dims deliveries over from Cheetah cxfs to LION
# Root needs to have rssh client key for lion configured - see 
# Catalogue documentation for details.
#
# You should add an entry like this to root's crontab to run this at intervals
# you prefer. 
# e.g.
# Job will run each minute 
# */1 * * * * /usr/local/bin/sac/sync_dims_deliveries
#
#Add a lock file to /tmp that indicates if a sync is in progress, if it is
#exit so that we dont try to run two concurrent rsyncs.
LOCKFILE=/tmp/dims-deliveries-sync-to-lion.lock
if [ -f "$LOCKFILE" ] #skip if exists
then
  echo "Skipping (already processing): $LOCKFILE"
else
  touch $LOCKFILE
  rsync -ave ssh /cxfs/eods/deliveries lion:/mnt/cataloguestorage2/filedrop/
  rm $LOCKFILE
fi
# be very very careful if you change this / enable this
# find /cxfs/datapickup/filedrop -name "*" -mtime +8 -exec rm -f {} \;

```

Finally add a line to the crontab:

```
sudo crontab -e
```

And add this line:

```
# Job will run at 1 minute intervalse to sync dims deliveries to lion
*/1 * * * * /usr/local/bin/sac/sync_dims_deliveries
```

Lastly, if you intend to make deliveries directly downloadable, you need to
share the delivery directory on the catalogue server. The configuration
disallows directory listings so that users cannot download products destined
for other users. Adding the following to 000-defult apache site makes the 
deliveries directory listable:

```
  Alias /deliveries /mnt/cataloguestorage2/filedrop/deliveries
  <Directory /mnt/cataloguestorage2/filedrop/deliveries>
    # for debugging only, show directory listings
    # Options Indexes FollowSymLinks MultiViews
    # in production, hide directory listings
    Options -Indexes FollowSymLinks MultiViews

    AllowOverride None
    Order allow,deny
    allow from all
  </Directory>

```


=== Lion Cron Jobs ===

On the lion server side, a similar cron job is run to:
- ingest any new packages that have arrived
- clear away any filedrop files older than 7 days
-

The cron job should not be run as root in order to avoid any potential side
effects that may occur from broken scripts etc.


```
# be very very careful if you change this!
# avoid the .ssh dir and other user profile stuff
find /mnt/cataloguestorage2/filedrop -name "*" -mtime +8 -exec rm -f {} \;
```
