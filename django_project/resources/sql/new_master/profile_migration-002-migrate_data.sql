BEGIN;

-- migrate user profiles
INSERT INTO useraccounts_sansauserprofile (
  user_id, strategic_partner, url, about, address1, address2, address3,
  address4, post_code, organisation, contact_no, mugshot,privacy)
SELECT
  catalogue_sacuserprofile.user_id,
  catalogue_sacuserprofile.strategic_partner,
  catalogue_sacuserprofile.url,
  catalogue_sacuserprofile.about,
  catalogue_sacuserprofile.address1,
  catalogue_sacuserprofile.address2,
  catalogue_sacuserprofile.address3,
  catalogue_sacuserprofile.address4,
  catalogue_sacuserprofile.post_code,
  catalogue_sacuserprofile.organisation,
  catalogue_sacuserprofile.contact_no,
  '',
  'closed'
FROM
  public.catalogue_sacuserprofile;

-- populate signup information
INSERT INTO userena_userenasignup (user_id, activation_key, activation_notification_send, email_unconfirmed, email_confirmation_key, email_confirmation_key_created)
SELECT catalogue_sacuserprofile.user_id, 'ALREADY_ACTIVATED', FALSE, '' ,'', now() FROM catalogue_sacuserprofile;

-- fix auth_user first_name, last_name
UPDATE auth_user set first_name=new_name, last_name=new_surname FROM (
  SElect user_id, coalesce(firstname,first_name) as new_name,coalesce(surname,last_name) as new_surname
  from catalogue_sacuserprofile inner join auth_user on auth_user.id = catalogue_sacuserprofile.user_id) as newnames
WHERE auth_user.id = user_id;
COMMIT;