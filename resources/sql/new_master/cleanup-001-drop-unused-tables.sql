BEGIN;

-- djangodblog

DROP TABLE djangodblog_error CASCADE;
DROP TABLE djangodblog_errorbatch CASCADE;

-- sentry
DROP TABLE sentry_filtervalue CASCADE;
DROP TABLE sentry_groupedmessage CASCADE;
DROP TABLE sentry_message CASCADE;
DROP TABLE sentry_messagecountbyminute CASCADE;
DROP TABLE sentry_messagefiltervalue CASCADE;
DROP TABLE sentry_messageindex CASCADE;

COMMIT;
