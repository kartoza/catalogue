Developer Guide
-----------------------------------------

Set your ssh config up
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get started, first add an entry like this to your ssh config file in ~/.ssh/config:

```
Host linfiniti2
  Port 8697
  HostName 188.40.123.80
  FallBackToRsh no
```

Checkout Sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Then setup a working dir and check out the sources (you can adapt dirs / paths
as needed, using these paths will keep you consistent with all setup notes but
its not required).

```
cd /home
sudo mkdir web
sudo chown -R <username>.<username> web
cd web
mkdir sac
```

Now you can check out either from linfiniti's repo:

```
git clone git@linfiniti2:sac_catalogue.git sac_catalogue
```

or from SANSA's repo:

```
git clone git@orasac1:sac_catalogue.git sac_catalogue
```


Then follow the instructions in README, skipping sections on informix, building
gdal from source and source code checkout (you already checked it out if you
have the readme :-)

Load a database dump
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A recent database dump can be obtained from:

```
http://196.35.94.243/sac_postgis_01February2011.dmp
```

Working with Git
------------------------------------------

Each devloper works on a remote branch, others can track a specific branch
locally and try out implemented features. After approving implementation,
branch is merged with HEAD. (possibly closed/removed from tree)

This commands are based on http://www.eecs.harvard.edu/~cduan/technical/git/


Getting a list of branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For local branches do:

```
git branch -v
```

For remote branches do:

```
git branch -r -v
```

To create remote branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For current versions of git (at least git 1.7 or better). Say we want to create
a new branch called 'docs-branch':

```
git branch docs-branch
git push --set-upstream origin docs-branch
git checkout docs-branch
```


Working with a remote branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to work with a remote branch locally (if it already exists
remotely), we must create local branch and setup tracking of remote branch. 

```
git pull #your local repo must be up to date first
git branch --track new-branch origin/new-branch
git checkout new-branch
```

Now you can go on to do your work in that branch.

To pull changes from remote repo do:

```
git pull origin
```

Deleting branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you are done with a branch, you can delete it. For a local branch do:

```
git branch -d new-branch
```

To delete a remote branch do (after first deleting it locally):

```
git push origin :new-branch
```

Distributed Git Repository Topology
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The repositories are arranged like this:

[img/git-topology.png]

The orasac master repo must pull from the linfiniti2 server at regular (e.g.
weekly) intervals using a command like this:

```
cd /opt/git/sac_catalogue
git pull git@linfiniti2:sac_catalogue.git

```

If changes have happened on the SAC side and committed to the repository on
orasac1, those changes should be pushed over to the catalogue on linfiniti2 so
that the two repos are in sync:

```
cd /opt/git/sac_catalogue
git push git@linfiniti2:sac_catalogue.git
```


Note that orasac1 also has an entry in /home/timlinux/.ssh/config like this:

```
Host linfiniti2
  HostName 188.40.123.80
  User timlinux
  Port 8697

```

The lion live and test instances are cloned from the orasac1 repo like this:

```
git clone git@orasac1:sac_catalogue.git sac_live
git clone git@orasac1:sac_catalogue.git sac_test
```

The instance on linfiniti2 gitosis was cloned in the same way into
/opt/git/repositories/sac_catalogue.

For the Tim / Drazen / Alessandro clones, the clone was carried out as
described in the first section of this doc.


Tracking branches from linfiniti with a master checkout from orasac
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this scenario, we want to be tracking master from orasac1 but occationally
pulling down branches from linfiniti2 to test them under
lion:/opt/sac_catalogue/sac_test. Make sure you have a linfiniti2 entry in your
~/.ssh/config as described further up in this document.

```
git remote add linfiniti2 git@linfiniti2:sac_catalogue.gi
git fetch linfiniti2
```

You should see something like the output below showing you that the branches
from the secondary remote repository:

```
The authenticity of host '[188.40.123.80]:8697 ([188.40.123.80]:8697)' can't be established.
RSA key fingerprint is cd:86:2b:8c:45:61:ae:15:13:45:95:25:8e:9a:6f:c4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[188.40.123.80]:8697' (RSA) to the list of known hosts.
 _ _        __ _       _ _   _ 
| (_)_ __  / _(_)_ __ (_) |_(_)
| | | '_ \| |_| | '_ \| | __| |
| | | | | |  _| | | | | | |_| |
|_|_|_| |_|_| |_|_| |_|_|\__|_|
 
 -- Authorized Access Only --                              
Enter passphrase for key '/home/timlinux/.ssh/id_dsa': 
remote: Counting objects: 201, done.
remote: Compressing objects: 100% (150/150), done.
remote: Total 150 (delta 103), reused 0 (delta 0)
Receiving objects: 100% (150/150), 1.10 MiB | 47 KiB/s, done.
Resolving deltas: 100% (103/103), completed with 28 local objects.
From linfiniti2:sac_catalogue
 * [new branch]      ale        -> linfiniti2/ale
 * [new branch]      ale_test   -> linfiniti2/ale_test
 * [new branch]      map_resize -> linfiniti2/map_resize
 * [new branch]      master     -> linfiniti2/master
 * [new branch]      tim-model-refactor-off-ale -> linfiniti2/tim-model-refactor-off-ale
`

```

Now we are ready to check out the branch from there e.g.:

```
git branch map_resize linfiniti2/map_resize
git pull #not sure if needed
git checkout map_resize
sudo /etc/init.d/apache2 reload
```

When you want to get back to the original again do:

```
git checkout origin/master
```

Tracking Linfiniti in your local repo and pushing changes to orasac1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this scenario, we want to have our master repo on the linfiniti development
server, and then periodically push changes over to orasac1 production repo. Our
checkout is on a third, deskop computer. So we do:

```
git clone git@linfiniti2:sac_catalogue.git sac_catalogue
```

That gives us a local repo whose remote master is on linfiniti. Now we add a
new remote (you can have multiple remote repos and sync between them):

```
git remote add orasac1 git@orasac1:sac_catalogue.git
git pull
```

Ok now our local repo is 'aware' of the remote repo on orasac1. So lets make a
branch that tracks master on orasac1:

```
git branch --track orasac1-master orasac1/master
git checkout orasac1-master
```

Now it is simple to pull changes down from linfiniti and push them over to orasac1:

```
git merge master
git push
```

Since the branch is tracking orasac1/master they will automatically get pushed there.

Alternatively, changes can be pushed over to orasac1 directly from in your local master branch:

```
git checkout master
git push orasac1 master
```

System logic and rules
------------------------------------------

Computation of geometric_accuracy_mean
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The spatial resolution of a product is calculated as the mean of its
spatial_resolution_x, spatial_resolution_y.

The values for spatial_resolution_x, spatial_resolution_y will vary per
sensor and per mode. According to the following table:

(SAC to provide required detail here).

------------ TABLE PLACEHOLDER -------------------


Sensor viewing angle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






The sensor viewing angle 




Updates and imports of products
------------------------------------------

vim /mnt/cataloguestorage/thumbnail_processing/thumb_blobs/lastblob.txt

Set desired blob no in above file.

python manage.py runscript --pythonpath=scripts -v 2 acs_importer
