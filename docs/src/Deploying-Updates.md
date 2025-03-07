---
title: SANSA Catalogue
summary: PROJECT_SUMMARY
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/kartoza/catalogue
copyright: Copyright 2023, PROJECT_OWNER
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#context_id: 1234
---

To deploy changes from git to live or test server:

```
cd /home/web/catalogue
source venv/bin/activate
cd django_project
git pull --rebase
python manage.py collectstatic --settings=core.settings.prod
```

Test server is online at http://41.74.158.4/
