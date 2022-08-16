Redmine Setup
------------------------------------------

Redmine is an issue tracking tool and is useful in general for project management as well as software development.

Redmine integrates with popular source management systems e.g. git, svn etc.

**Note:** You should use ruby 1.8! (Unless there is an update on redmine home page allowing otherwise)

```
sudo apt-get install redmine apache2 redmine-sqlite libapache2-mod-fcgid
sudo apt-get install libfcgi libfcgi-dev libfcgi-ruby1.8.1
sudo apt-get install ruby1.8-dev
sudo gem install fcgi
sudo a2enmod fcgid rewrite
```

Add the following to /etc/apache2/mods-enabled/fcgid.config

```
  #Next line added by Tim for Redmine
  SocketPath /tmp/fcgid_sock/

```

```
sudo ufw allow 80
sudo ufw status
```

Which should show:

```
Status: active

To                         Action      From
--                         ------      ----
22                         DENY        Anywhere
8697                       ALLOW       Anywhere
80                         ALLOW       Anywhere

25                         ALLOW OUT   Anywhere
```




Set up an apache config like this:

```
# (mod_fastcgi is much harder to configure)
# Configuration for http://localhost:8080
<VirtualHost *>
        ServerAdmin webmaster@localhost
        ServerName redmine.linfiniti.com
        # DefaultInitEnv for module mod_fcgid
        DefaultInitEnv RAILS_RELATIVE_URL_ROOT ""
        DefaultInitEnv X_DEBIAN_SITEID "default"

        # the mod_fcgid socket path
        # Tim: I added this to mods-available/fcgid.conf rather because it was giving an error when included here
        #SocketPath "/var/run/redmine/sockets/default"
        Alias "/plugin_assets/" /var/cache/redmine/default/plugin_assets/
        DocumentRoot /usr/share/redmine/public
        <Directory "/usr/share/redmine/public">
                Options +FollowSymLinks +ExecCGI
                Order allow,deny
                Allow from all
                RewriteEngine On
                RewriteRule ^$ index.html [QSA]
                RewriteRule ^([^.]+)$ $1.html [QSA]
                RewriteCond %{REQUEST_FILENAME} !-f [OR]
                RewriteCond %{REQUEST_FILENAME} dispatch.fcgi$
                RewriteRule ^(.*)$ dispatch.fcgi [QSA,L]
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/redmine.error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog ${APACHE_LOG_DIR}/redmine.access.log combined
</VirtualHost>

```


```
sudo /etc/init.d/apache2 reload
sudo dpkg-reconfigure redmine
```

I used the sqlite backend and took defaults or obvious choices through the package setup.

Default user: admin
Default password: admin


Git repository browsing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new project, and then go to the administration panel for it. Then choose

Repositories -> Type: Git 

Then enter the url to the .git directory e.g.

```
/opt/git/repositories/sac_catalogue.git/.git
```

Trac to Redmine Migration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do this before setting up email below.

```
sudo -u www-data X_DEBIAN_SITEID=default RAILS_ENV=production rake -f /usr/share/redmine/Rakefile redmine:migrate_from_trac --trace
```

Output (use similar responses to promptes):

```
** Invoke redmine:migrate_from_trac (first_time)
** Invoke environment (first_time)
** Execute environment
** Execute redmine:migrate_from_trac

WARNING: a new project will be added to Redmine during this process.
Are you sure you want to continue ? [y/N] y

Trac directory []: /opt/trac/sac
Trac database adapter (sqlite, sqlite3, mysql, postgresql) [sqlite]: sqlite3
Trac database encoding [UTF-8]: 
Target project identifier []: sansa-general

Migrating components................
Migrating milestones..
Migrating custom fields..
Migrating tickets.................................................................................................................................................................................................................................................................................................................................................
Migrating wiki..................

Components:      16/16
Milestones:      2/2
Tickets:         337/337
Ticket files:    37/38
Custom values:   443/443
Wiki edits:      18/18
Wiki files:      2/3

```

Mark the old trac as read only (put a note on the front page first):

```
cd /opt
sudo chmod -R ag-w trac
```

Redmine Email Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``sudo cp /usr/share/redmine/config/email.yml.example /etc/redmine/default/email.yml``

Now edit that file so it looks like this::
   
  production:
    delivery_method: :sendmail
    smtp_settings:
    address: 127.0.0.1
    port: 25

  development:
    delivery_method: :sendmail
    smtp_settings:
    address: 127.0.0.1
    port: 25

