Working with GIT
------------------------------------------

Hosting GIT Repos using gitosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See also [http://blog.agdunn.net/?p=277 this page]. The idea is that we set up
a single user account ('git') which proxies commit into the repo and has not
shell access. We then add each ssh key for each user that wants access to the
repo, assign the user to one or more groups and they can get busy.

Set up the server side
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Note:** The gitosis repos are hosted on 'orasac1'.

Assuming only your pub ssh key is in authorised keys:

```
sudo apt-get install gitosis
sudo adduser --system --shell /bin/sh --gecos 'git version control' \
             --group --disabled-password --home /opt/git git
sudo -H -u git gitosis-init < /home/timlinux/.ssh/authorized_keys2

```

Allow ssh access to git user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit /etc/ssh/sshd_config and add git to AllowUsers list then restart ssh:

```
sudo /etc/init.d/ssh restart
```

Check out gitosis admin on the client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
mkdir -p ~/dev/gitosis
cd ~/dev/gitosis
git clone git@orasac1:gitosis-admin.git sansa-gitosis-admin
```

Adding a user, group and project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
cd sansa-gitosis-admin
```

Now copy the users pub key into keydir naming it after the user@name listed in their key e.g.:

```
vim keydir/cstephens@cstephens-nb1.pub
```

In this example we are adding access to Casey (I will put him in the admin group too so that he can add more users later). The contents of his keyfile look like this (based on his ssh public key):

```
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3WKItKSQU3mtrXwq3P64XM9ChN+exWq69c/q1lWsi/X8yzfbMM9I3Ms
t+wbFmTS4rWWy2xU7H5ES1CeHo9QS6GECMJNSp5EiGSIKCmY3IEwaYuxg4TJVABXwCmJ3MSWRXOFMq1uooaiG4u5SKWQP
JWMgOh41RnEClxLoS2X6sweMPYFlURNTjLja2hCFDROxJaZ2+95/nvjkw2LxihTgeJOGUCmGvGGRHfwZK5HyehqxqZF
LrUjHjtzO5h3yOWgGhdjja12A7RHqLkrZtH7ftY9K8/4O2nAp2IpufWWi6LiGBQrk85bX4JhC/B3lQkbH1MiVM55Dzs
UJFr/xQuw+FQ== cstephens@cstephens-nb1
```

**Note:** The .pub extension is REQUIRED. Also line breaks added above to prevent 
page layout issues should not be included.

Then edit gitosis.conf. Add each admin user into the members list for the gitosis-admin group e.g.:

```
[gitosis]

[group gitosis-admin]
writable = gitosis-admin
members = tim@linfiniti.com cstephens@sansa.org.za

```

For a new project, add a new group and repo clause like this:

```
[group sac_catalogue_committers]
writable = sac_catalogue
members = tim@linfiniti.com cstephens@sansa.org.za

[repo sac_catalogue]
gitweb = no
description = SANSA Catalogue
owner = SANSA
daemon = no
```

**Note:** The .pub extension is not used in the conf file.

We will add entries for the sansa fork of QGIS too (we will need to add Christoph and Riaan to this group).

```
[group sansa_qgis_committers]
writable = sac_catalogue
members = tim@linfiniti.com cstephens@sansa.org.za

[repo qgis]
gitweb = no
description = SANSA Catalogue
owner = SANSA
daemon = no

```

**Note:** The writeable list in each group should contain a list of those repos
that members of that group can write (commit) to. Typically you will want to
give the gitosis admin group write permissions to all repos, so each time you
add a new repo, update the group like this:

```
[group gitosis-admin]
writable = gitosis-admin sac_catalogue qgis
```

To add a user to an existing project follow the steps above, but just append
their key name to the members list.

Now and the new files, commit and push:

```
git add keydir/*
git add gitosis.conf
git commit -m "Set up project for SANSA Catalogue"
git push
```




Create a new empty gitosis hosted repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last step is to actually create the repo we defined above (in this case
sac_catalogue) and push it up to the server.

```
cd /home/web
mkdir sac_catalogue
cd sac_catalogue
git init
git add .
git remote add origin git@orasac1:sac_catalogue.git
git commit
```

You need to add something to your repo before trying to push it up to the
master, so I just put in a .gitignore to start, commit it then push up.

```
touch .gitignore
git add .gitignore
git commit -m "Added ignore file"
git push origin master
```

You should get a message like:

```
Counting objects: 3, done.
Writing objects: 100% (3/3), 221 bytes, done.
Total 3 (delta 0), reused 0 (delta 0)
To git@orasac1:sac_catalogue.git
 * [new branch]      master -> master
```

If you got something like this instead:

```
# git push origin master
error: src refspec master does not match any.
fatal: The remote end hung up unexpectedly
```

Its just a symptom that your repo is empty. Add the .gitignore, commit it
locally and then try to push it up to the server again.


**Note**: It is possible to provide anonymous access to this repo too using
git-daemon. See the article mentioned at the start of this section for more
info.

Checkout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally you can check out your repo e.g. on a different computer:

```
git clone git@orasac1:sac_catalogue.git
```

Hosting a clone of an upstream repo in gitosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here we want to host a copy of a git repository from upstream and make it available 
to internal SANSA developers. We will check out the linfiniti git repo in this case:

(On orasac1)

```
sudo su - git
bash
cd repotositories
vim ~/.ssh/config
```

Add the following to the ssh config for git user (we have configured read only access for this user):

```
Host linfiniti2
  User git
  Port 8697
  HostName 188.40.123.80
  FallBackToRsh no

```

Now clone the upstream repo:


```

git@orasac01:~/repositories$ git clone --bare git@linfiniti2:qgis.git
```


On your local machine, you can now clone QGIS, work on it, commit your changes to orasac1. When you would like your changes to be merged into QGIS, you email a pull request to linfiniti, we then pull your changes and commit them to svn. To keep the orasac1 copy 'fresh' (synchronised with upstream) a cron job should be configure to pull changes regularly to it.

Check out an existing repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


You should not need to do the above for the QGIS and SANSA Catalogue projects since they already exist and are populated. Above process is for when you want to create a new, empty repo.


The sac_catalogue sources can be checked out like this:

```
git clone git@orasac1:sac_catalogue.git sac_catalogue

```

Similarly the SANSA QGIS fork can be checked out like this:

```
git clone git@orasac1:qgis.git qgis
```



Working with Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
git remote add orasac1 git@orasac1:sac_catalogue
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


