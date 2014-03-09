#!/bin/python
"""Fabric script for Catalgoue."""
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
from fabric.api import run, sudo, env, hide, cd, task, fastprint
from fabric.colors import red, magenta, yellow, cyan
from fabric.contrib.files import contains, exists, append, sed
from fabric.context_managers import quiet
import fabtools
from fabgis import postgres, common, virtualenv, git, umn_mapserver
# Don't remove even though its unused
#noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

# Usage fab localhost [command]
#    or fab remote [command]
#  e.g. fab localhost update

# This will get replaced in various places, for a generic site, it may be
# all you need to change...
PROJECT_NAME = 'catalogue'
#env.user = 'vagrant'


def _all():
    """Things to do regardless of whether command is local or remote."""

    # Key is hostname as it resolves by running hostname directly on the server
    # value is desired web site url to publish the repo as.

    repo_site_names = {
        'spur': '%s.localhost' % PROJECT_NAME,
        'waterfall': '%s.localhost' % PROJECT_NAME,
        'maps.linfiniti.com': '%s.linfiniti.com' % PROJECT_NAME,
        'testcatalogue2': 'test.catalogue.sansa.org.za',
        # vagrant vm
        'catalogue': '%s.localhost' % PROJECT_NAME}

    with hide('output'):
        env.user = run('whoami')
        env.hostname = run('hostname')
        if env.hostname not in repo_site_names:
            print 'Error: %s not in: \n%s' % (env.hostname, repo_site_names)
            exit()
        else:
            # sitename for apache venv
            env.repo_site_name = repo_site_names[env.hostname]
            # where to check the repo out to
            env.webdir = '/home/web'
            # repo uri
            env.git_url = 'https://github.com/timlinux/%s.git' % PROJECT_NAME
            # checkout name for repo
            env.repo_alias = PROJECT_NAME
            # user wsgi should run as (will be created if needed)
            env.wsgi_user = 'catalogue'
            # Deploy dir - e.g. /home/web/foo
            env.code_path = os.path.join(env.webdir, env.repo_alias)
            show_environment()

###############################################################################
# Next section contains helper methods tasks
###############################################################################


@task
def rsync_vagrant_to_code_dir():
    """Rsync from vagrant mount to code dir."""
    _all()
    with cd('/home/web/'):
        sudo('rsync -va /vagrant/ %s/ --exclude \'venv\' '
                '--exclude \'*.pyc\' --exclude \'.git\'' % PROJECT_NAME)
    collect_static()


@task
def collect_static():
    _all()
    with cd('%s/django_project' % env.code_path):
        run('../venv/bin/python manage.py collectstatic --noinput')
        wsgi_file = 'core/wsgi.py'
        sudo('find . -iname \'*.pyc\' -exec rm {} \;')
        run('touch %s' % wsgi_file)


def replace_tokens(conf_file):
    if '.templ' == conf_file[-6:]:
        conf_file = conf_file.replace('.templ', '')

    run(
        'cp %(conf_file)s.templ %(conf_file)s' % {
            'conf_file': conf_file})
    # We need to replace these 3 things in the conf file:
    # [SERVERNAME] - web site base url e.g. foo.com
    # [ESCAPEDSERVERNAME] - the site base url with escaping e.g. foo\.com
    # [SITEBASE] - dir under which the site is deployed e.g. /home/web
    # [SITENAME] - should match env.repo_alias
    # [SITEUSER] - user apache wsgi process should run as
    # [CODEBASE] - concatenation of site base and site name e.g. /home/web/app
    escaped_name = env.repo_site_name.replace('.', '\\\.')
    fastprint('Escaped server name: %s' % escaped_name)
    sed('%s' % conf_file, '\[SERVERNAME\]', env.repo_site_name)
    sed('%s' % conf_file, '\[ESCAPEDSERVERNAME\]', escaped_name)
    sed('%s' % conf_file, '\[SITEBASE\]', env.webdir)
    sed('%s' % conf_file, '\[SITENAME\]', env.repo_alias)
    sed('%s' % conf_file, '\[SITEUSER\]', env.wsgi_user)
    sed('%s' % conf_file, '\[CODEBASE\]', env.code_path)


def setup_mapserver():
    # Clone and replace tokens in mapserver map file
    # Clone and replace tokens in mapserver conf
    umn_mapserver.setup_mapserver()
    conf_dirs = [
        '%s/resources/server_config/mapserver/mapfiles/' % env.code_path,
        '%s/resources/server_config/mapserver/apache-include/' % (
            env.code_path)]
    for conf_dir in conf_dirs:
        output = run('ls %s' % conf_dir)
        files = output.split()
        for myFile in files:
            ext = os.path.splitext(myFile)[1]
            conf_file = os.path.join(conf_dir, myFile)

            if ext == '.templ':
                replace_tokens(conf_file)


def setup_website():
    """Initialise or update the git clone.

    e.g. to update the server

    fab -H 10.1.1.0:8697 remote setup_website

    or if you have configured env.hosts, simply

    fab remote setup_website
    """

    fabtools.require.postfix.server(env.repo_alias)
    fabtools.require.deb.package('libapache2-mod-wsgi')
    # Find out if the wsgi user exists and create it if needed e.g.
    fabtools.require.user(
        env.wsgi_user,
        create_group=env.wsgi_user,
        system=True,
        comment='System user for running the wsgi process under')

    if not exists(env.webdir):
        sudo('mkdir -p %s' % env.plugin_repo_path)
        sudo('chown %s.%s %s' % (env.user, env.user, env.webdir))

    # Clone and replace tokens in apache conf

    conf_file = (
        '%s/resources/server_config/apache/%s.apache.conf' % (
            env.code_path, env.repo_alias))

    run(
        'cp %(conf_file)s.templ %(conf_file)s' % {
            'conf_file': conf_file})

    replace_tokens(conf_file)

    with cd('/etc/apache2/sites-available/'):
        if exists('%s.apache.conf' % env.repo_alias):
            sudo('a2dissite %s.apache.conf' % env.repo_alias)
            fastprint('Removing old apache2 conf', False)
            sudo('rm %s.apache.conf' % env.repo_alias)

        sudo('ln -s %s .' % conf_file)

    # wsgi user needs pg access to the db
    postgres.require_postgres_user(env.wsgi_user, env.wsgi_user)
    postgres.require_postgres_user('timlinux', 'timlinux')
    postgres.require_postgres_user('readonly', 'readonly')
    postgres.create_postgis_1_5_db('catalogue', env.wsgi_user)
    grant_sql = 'grant all on schema public to %s;' % env.wsgi_user
    # assumption is env.repo_alias is also database name
    run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL TABLES IN schema public to %s;' % env.wsgi_user)
    # assumption is env.repo_alias is also database name
    run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL SEQUENCES IN schema public to %s;' % env.wsgi_user)
    run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    pwd_sql = 'ALTER USER timlinux WITH PASSWORD \'timlinux\';'
    run('psql %s -c "%s"' % (env.repo_alias, pwd_sql))
    #with cd(env.code_path):
        # run the script to create the sites view
        #run('psql -f sql/3-site-view.sql %s' % env.repo_alias)

    # Add a hosts entry for local testing - only really useful for localhost
    hosts = '/etc/hosts'
    if not contains(hosts, env.repo_site_name):
        append(hosts, '127.0.0.1 %s' % env.repo_site_name, use_sudo=True)
    if not contains(hosts, 'www.' + env.repo_site_name):
        append(hosts,
               '127.0.0.1 %s' % 'www.' + env.repo_site_name,
               use_sudo=True)
        # Make sure mod rewrite is enabled
    sudo('a2enmod rewrite')
    # Enable the vhost configuration
    sudo('a2ensite %s.apache.conf' % env.repo_alias)

    # Check if apache configs are ok - script will abort if not ok
    sudo('/usr/sbin/apache2ctl configtest')
    sudo('a2dissite default')
    fabtools.require.service.restarted('apache2')

    #Setup a writable media dir for apache
    media_path = '%s/django_project/core/media' % env.code_path
    if not exists(media_path):
        sudo('mkdir %s' % media_path)
        sudo('chown %s.%s %s' % (env.wsgi_user, env.wsgi_user, env.code_path))


def setup_venv():
    """Initialise or update the virtual environmnet.


    To run e.g.::

        fab -H 188.40.123.80:8697 remote setup_venv

    or if you have configured env.hosts, simply

        fab remote setup_venv
    """

    virtualenv.setup_venv(env.code_path, requirements_file='REQUIREMENTS.txt')
    virtualenv.build_pil(env.code_path)
    virtualenv.build_python_gdal(env.code_path)

    # Run again to check all is up to date
    with cd(env.code_path):
        run('venv/bin/pip install -r REQUIREMENTS.txt')


@task
def update_git_checkout(branch='master'):
    """Make sure there is a read only git checkout.

    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'

    To run e.g.::

        fab -H 188.40.123.80:8697 update_git_checkout


    """
    _all()
    git.update_git_checkout(
        env.webdir, env.git_url, env.repo_alias, branch=branch)
    #run('./runcollectstatic.sh')
    wsgi_file = '%s/django_project/core/wsgi.py' % env.code_path
    run('touch %s' % wsgi_file)

###############################################################################
# Next section contains actual tasks
###############################################################################


@task
def get_dump():
    """Get a dump of the database from the server."""
    _all()
    postgres.get_postgres_dump(env.repo_alias, ignore_permissions=True)


@task
def restore_dump(file_name=None, migrations=False):
    """Upload dump to host, remove existing db, recreate then restore dump."""
    _all()
    postgres.restore_postgres_dump(
        env.repo_alias,
        ignore_permissions=True,
        file_name=file_name,
        user=env.wsgi_user,
        password=env.wsgi_user)
    if migrations:
        run_migrations()


@task
def run_migrations():
    _all()
    grant_sql = ('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %s;'
                 % env.wsgi_user)
    # assumption is env.repo_alias is also database name
    run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    with cd('/home/web/catalogue/django_project/'):
        run('../venv/bin/python manage.py migratev3 '
            '--settings=core.settings.project')


@task
def deploy(branch='master'):
    """Do a fresh deployment of the site to a server.

    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'.

    To run e.g.::

        fab -H 188.40.123.80:8697 deploy

        or to package up a specific branch (in this case v1)

        fab -H 88.198.36.154:8697 deploy:v1

    For live server:

        fab -H 5.9.140.151:8697 deploy

    """

    fastprint(cyan('Catalogue deploy task started...\n'))
    with quiet():
        common.add_ubuntugis_ppa()
        ## fabgis.setup_postgis()
    fastprint(cyan('Setting up PostGIS...\n'))
    with quiet():
        postgres.setup_postgis_2()
    fastprint(cyan('Setting up packages...\n'))
    with quiet():
        fabtools.require.deb.package('subversion')
        fabtools.require.deb.package('python-pip')
        fabtools.require.deb.package('libxml2-dev')
        fabtools.require.deb.package('libxslt1-dev')
        fabtools.require.deb.package('python-dev')
        fabtools.require.deb.package('build-essential')
        fabtools.require.deb.package('libgdal1-dev')
        fabtools.require.deb.package('gdal-bin')
        fabtools.require.deb.package('curl')
    fastprint(cyan('Updating GIT checkout...\n'))
    # We can't use 'with_quiet' as this suppresses the prompt for
    # username/password
    update_git_checkout(branch)
    fastprint(cyan('Setting up venv...\n'))
    with quiet():
        setup_venv()
    fastprint(cyan('Setting up website...\n'))
    with quiet():
        setup_website()
    fastprint(cyan('Setting up mapserver...\n'))
    with quiet():
        setup_mapserver()
    if not fabtools.service.is_running('apache2'):
        fastprint(red(
            'Apache is not running - you may need to log in to '
            'start it manually.\n'))
    fastprint(cyan(
        'TODO: Set the allowed hosts in '
        'django_project/core/settings/prod.py to have the ip '
        'address and the host name for this server. Also replace '
        'vagrant user / password in '
        'django_project/core/settings/project.py with '
        'catalogue/catalogue.'))
    fastprint(magenta(
        'TODO: set the following permissions on the db:\n'
        'GRANT ALL ON SCHEMA public TO catalogue;\n'
        'GRANT ALL ON ALL TABLES IN SCHEMA public TO catalogue;\n'
        'GRANT ALL ON ALL TABLES IN SCHEMA public TO catalogue;\n'))
    fastprint(magenta(
        'TODO: install nodeenv, npm and yuglify then collect static \n'
        'Ideally install something like:\n'
        'source venv/bin/activate\n'
        'pip install nodeenv\n'
        'nodeenv venv --node=0.8.15\n'
        'env/bin/npm -g install yuglify\n'
        '\n'
        'But that didnt work well so I did:\n'
        'sudo apt-get install node\n'
        'sudo apt-get install npm\n'
        'sudo npm -g install yuglify\n'
        'python manage.py collectstatic --settings=core.settings.prod\n'
    ))


@task
def server_to_debug_mode():
    """Put the server in debug mode (normally not recommended)."""
    _all()
    fastprint(cyan('Putting server into debug mode.\n'))
    config_file = os.path.join(
        env.code_path, 'django_project', 'core', 'settings', 'project.py')
    sed(
        config_file,
        'DEBUG = TEMPLATE_DEBUG = False',
        'DEBUG = TEMPLATE_DEBUG = True')
    with cd(os.path.join(env.code_path, 'django_project')):
        run('touch core/wsgi.py')
    fastprint(red('Warning: your server is now in DEBUG mode!\n'))


@task
def server_to_production_mode():
    """Put the server in production mode (recommended)."""
    _all()
    fastprint(cyan('Putting server into PRODUCTION mode.\n'))
    config_file = os.path.join(
        env.code_path, 'django_project', 'core', 'settings', 'project.py')
    sed(
        config_file,
        'DEBUG = TEMPLATE_DEBUG = True',
        'DEBUG = TEMPLATE_DEBUG = False')
    with cd(os.path.join(env.code_path, 'catalogue')):
        run('touch core/wsgi.py')
    fastprint(magenta('Note: your server is now in PRODUCTION mode!'))

@task
def show_environment():
    """For diagnostics - show any pertinent info about server."""
    fastprint('\n-------------------------------------------------\n')
    fastprint(cyan('User      : %s\n' % env.user))
    fastprint(cyan('Host      : %s\n' % env.hostname))
    fastprint(cyan('Site Name : %s\n' % env.repo_site_name))
    fastprint(cyan('Dest Path : %s\n' % env.webdir))
    fastprint(cyan('Wsgi User : %s\n' % env.wsgi_user))
    fastprint(cyan('Git  Url  : %s\n' % env.git_url))
    fastprint(cyan('Repo Alias: %s\n' % env.repo_alias))
    fastprint(cyan('-------------------------------------------------\n'))
