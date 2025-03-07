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

When you run the live system, you need to run the LibreOffice headless backend for generating reports.

You can run in the foreground like this for testing:
```
soffice '--accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' --headless
```

Or to run in the background for production you should probably add it to the server boot sequence (e.g. in /etc/rc.local) so that it runs on first boot.

```
# Added by Tim for Catalogue report printing backend
soffice '--accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' --headless & 
```

Verify that it is running:

```
ps -ef | grep soffice
```

Should produce something like this:


```
root      1335  1230  0 17:10 ?        00:00:00 /usr/lib/libreoffice/program/soffice.bin --accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService --headless
```

Then test by producing a pdf report on the server.
