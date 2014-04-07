# Running tests:

## Preparation

Make sure you have the base sac-master database in place:

```
createdb sac-master -T template_postgis
```

Or copy ``django_project/core/jenkins.py`` to e.g.
``django_project/core/jenkins_timlinux.py`` and use it in place of jenkins
below.

## Collect static

You need to have node-venv, npm and yuglify installed in your venv. Note
that if you are behind a proxy you also need to do:

```
venv/bin/activate
npm config set proxy http://192.168.2.2:3128
npm config set https-proxy http://192.168.2.2:3128
```

Then do:

```
cd django_project
python manage.py collectstatic --settings=core.settings.dev_timlinux
```

## Jenkins

To run the full test suite using the jenkins runner:

```bash
python manage.py jenkins --settings=core.settings.jenkins
```

Or using your own jenkins config

```bash
python manage.py jenkins --settings=core.settings.jenkins_timlinux
```

## Django Test runner

To run using the django test runner:

```bash
python manage.py test catalogue --settings=core.settings.test_timlinux
```

To run an individual module:

```bash
python manage.py test catalogue.tests.test_dims_iif_ingestor \
--settings=core.settings.test_timlinux
```

To run an individual module:

```bash
python manage.py test catalogue.tests.test_dims_iif_ingestor.DIMSIIDIngestorTest \
--settings=core.settings.test_timlinux
```

## Running tests in pycharm

To run tests in pycharm (you need the pro version) create run
configurations based on the django test base configuration (you must have
registered your pycharm project as a django project):

Run all tests:

```
Name: All Catalogue Test
Target: catalogue
Custom Settings: /home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py
Working Directory: /home/timlinux/dev/python/catalogue
```

To run an individual module:

```
Name: Test IIF Ingestors
Target: catalogue.tests.test_dims_iif_ingestor
Custom Settings: /home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py
Working Directory: /home/timlinux/dev/python/catalogue
```


# WebODT

Since no-one else has added a README for the catalogue, repo, I'm going to hijack it!
This is information regarding the use of django-webodt for producing PDF and other
documents for the Catalogue's reporting requirements.

At this stage (21st August 2013), the functionality is in place, but some aesthetic
work is still required in the templates. Further work may also be required for producing
XLS or CSV reports.

## Requirements

django-webodt uses LibreOffice as the backend to run the conversion. Therefore,
the system running the Catalogue (including local test servers) must have LibreOffice
installed and running - either daemonized or by starting from the command line.

* Install LibreOffice `sudo apt-get install libreoffice` and, to be safe, `sudo apt-get install python-uno`
* Setup LibreOffice as a demon process OR run the following command:

```sh
soffice '--accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' --headless
```

* If necessary: `pip install django-webodt`

## Usage

Report templates must be saved in `django_project/reports/report-templates`

**We have hijacked the existing PDF trigger in `renderWith`. This means that all you need to do in order
to render a PDF from a view is add `?pdf` to the URL, e.g. `/ordermonthlyreport/2013/08/?pdf`. There must
be an odt template in `django_project/reports/report-templates` with exactly the same name as the html template
used in the standard view**

If you need to generate a PDF within a function (such as to attach to an email):

django-webodt ships with a shortcut command into which we pass parameters; the shortcut
creates the file as specified in the parameters. Here is an example usage:

(Note: I've imported the shortcut as `renderReport` in order to avoid confusion with
Django's `render_to_response` shortcut)

```python
from webodt.shortcuts import render_to_response as renderReport

@staff_member_required
def renderVisitorListPDF(theRequest):
    myRecords = Visit.objects.order_by('-visit_date')
    return renderReport('visitor-list.odt',
                     context_instance=RequestContext(theRequest),
                     format='pdf',
                     filename='visitor-list.pdf',
                     dictionary={'myRecords': myRecords})
```

The shortcut always returns a file object. In this case, the view is
called by a URL and the view returns that file object, triggering a file download
in the user's browser.

This is useful in the case of emailing the output, as in `catalogue.views.helpers.notifySalesStaff`.
Here, the output can be directly attached to the outgoing email:

```python
theOrderPDF = renderPDF('order-summary.odt',
                            dictionary={'myOrder': myOrder,
                                       'myRecords': myRecords,
                                       'myHistory': myHistory},
                            format='pdf',
                            filename='order-summary.pdf')
.....
myMsg.attach_related_file(theOrderPDF)
```

## The Templates

The templates must be edited in LibreOffice. They can be treated as standard LibreOffice
documents incorporating tables, images and footer/header text. Please use the included
base-template.odt as your starting point in order to ensure that the content borders
are correct.

Most standard Django template tags can be used in the templates. Please see this doc
for information on rendering tables:

[Rendering tables in webodt](https://github.com/NetAngels/django-webodt/blob/master/doc/tables.rst)
