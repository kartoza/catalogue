# Intro

Since no-one else has added a README for the catalogue, repo, I'm going to hijack it!
This is information regarding the use of django-webodt for producing PDF and other
documents for the Catalogue's reporting requirements.

At this stage (21st August 2013), the functionality is in place, but some aesthetic
work is still required in the templates. Further work may also be required for producing
XLS or CSV reports.

# Requirements

django-webodt uses LibreOffice as the backend to run the conversion. Therefore,
the system running the Catalogue (including local test servers) must have LibreOffice
installed and running - either daemonized or by starting from the command line.

* Install LibreOffice `sudo apt-get install libreoffice-common`
* Setup LibreOffice as a demon process OR run the following command:

```sh
soffice '--accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' --headless
```

* If necessary: `pip install django-webodt`

# Usage

Report templates must be saved in django_project/reports/report-templates

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

Please see visitor-list.odt to see how the table is rendered.

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

# The Templates

The templates must be edited in LibreOffice. They can be treated as standard LibreOffice
documents incorporating tables, images and footer/header text. Please use the included
base-template.odt as your starting point in order to ensure that the content borders
are correct.

Most standard Django template tags can be used in the templates. Please see this doc
for information on rendering tables:

[Rendering tables in webodt](https://github.com/NetAngels/django-webodt/blob/master/doc/tables.rst)
