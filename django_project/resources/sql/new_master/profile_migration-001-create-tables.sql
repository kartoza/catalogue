BEGIN;

-- userena
CREATE TABLE "userena_userenasignup" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "last_active" timestamp with time zone,
    "activation_key" varchar(40) NOT NULL,
    "activation_notification_send" boolean NOT NULL,
    "email_unconfirmed" varchar(75) NOT NULL,
    "email_confirmation_key" varchar(40) NOT NULL,
    "email_confirmation_key_created" timestamp with time zone
)
;

-- guardian

CREATE TABLE "guardian_userobjectpermission" (
    "id" serial NOT NULL PRIMARY KEY,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_pk" varchar(255) NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id", "content_type_id", "object_pk")
)
;
CREATE TABLE "guardian_groupobjectpermission" (
    "id" serial NOT NULL PRIMARY KEY,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_pk" varchar(255) NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id", "content_type_id", "object_pk")
)
;
CREATE INDEX "guardian_userobjectpermission_permission_id" ON "guardian_userobjectpermission" ("permission_id");
CREATE INDEX "guardian_userobjectpermission_content_type_id" ON "guardian_userobjectpermission" ("content_type_id");
CREATE INDEX "guardian_userobjectpermission_user_id" ON "guardian_userobjectpermission" ("user_id");
CREATE INDEX "guardian_groupobjectpermission_permission_id" ON "guardian_groupobjectpermission" ("permission_id");
CREATE INDEX "guardian_groupobjectpermission_content_type_id" ON "guardian_groupobjectpermission" ("content_type_id");
CREATE INDEX "guardian_groupobjectpermission_group_id" ON "guardian_groupobjectpermission" ("group_id");

-- easythumbnails

CREATE TABLE "easy_thumbnails_source" (
    "id" serial NOT NULL PRIMARY KEY,
    "storage_hash" varchar(40) NOT NULL,
    "name" varchar(255) NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    UNIQUE ("storage_hash", "name")
)
;
CREATE TABLE "easy_thumbnails_thumbnail" (
    "id" serial NOT NULL PRIMARY KEY,
    "storage_hash" varchar(40) NOT NULL,
    "name" varchar(255) NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "source_id" integer NOT NULL REFERENCES "easy_thumbnails_source" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("storage_hash", "name", "source_id")
)
;
CREATE INDEX "easy_thumbnails_source_storage_hash" ON "easy_thumbnails_source" ("storage_hash");
CREATE INDEX "easy_thumbnails_source_storage_hash_like" ON "easy_thumbnails_source" ("storage_hash" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_source_name" ON "easy_thumbnails_source" ("name");
CREATE INDEX "easy_thumbnails_source_name_like" ON "easy_thumbnails_source" ("name" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_storage_hash" ON "easy_thumbnails_thumbnail" ("storage_hash");
CREATE INDEX "easy_thumbnails_thumbnail_storage_hash_like" ON "easy_thumbnails_thumbnail" ("storage_hash" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_name" ON "easy_thumbnails_thumbnail" ("name");
CREATE INDEX "easy_thumbnails_thumbnail_name_like" ON "easy_thumbnails_thumbnail" ("name" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_source_id" ON "easy_thumbnails_thumbnail" ("source_id");

-- sansauserprofile

CREATE TABLE "useraccounts_sansauserprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "mugshot" varchar(100) NOT NULL,
    "privacy" varchar(15) NOT NULL,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "strategic_partner" boolean NOT NULL,
    "url" varchar(200) NOT NULL,
    "about" text NOT NULL,
    "address1" varchar(255) NOT NULL,
    "address2" varchar(255) NOT NULL,
    "address3" varchar(255) NOT NULL,
    "address4" varchar(255) NOT NULL,
    "post_code" varchar(25) NOT NULL,
    "organisation" varchar(255) NOT NULL,
    "contact_no" varchar(16) NOT NULL
)
;


COMMIT;
