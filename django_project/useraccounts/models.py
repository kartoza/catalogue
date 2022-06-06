from django.db import models
from userena.models import UserenaBaseProfile


class SansaUserProfile(UserenaBaseProfile):
    """
    We define extra properties we want to store about users here - in
    particular if they belong to institutions that have strategic partnerships
    with SAC so that they may view hires spot data etc.
    """
    user = models.OneToOneField(
        'auth.User',
        unique=True,
        verbose_name='user',
        related_name='sansauserprofile',
        on_delete=models.CASCADE
    )
    strategic_partner = models.BooleanField(
        'Strategic Partner?', help_text=('Mark this as true if the person '
        'belongs to an institution that is a CSIR/SAC strategic partner'),
        default=False
    )
    url = models.URLField('Your website url', blank=True)
    about = models.TextField(blank=True)
    address1 = models.CharField(
        'Address 1 (required)', max_length=255, null=False, blank=False
    )
    address2 = models.CharField(
        'Address 2 (required)', max_length=255, null=False, blank=False
    )
    address3 = models.CharField(max_length=255, blank=True)
    address4 = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(
        'Post Code (required)', max_length=25, null=False, blank=False
    )
    organisation = models.CharField(
        'Organisation (required)', max_length=255, null=False, blank=False
    )
    contact_no = models.CharField(
        'Contact No (required)', max_length=16, null=False, blank=False
    )

    def first_name(self):
        """
        Proxy to main user model needed for admin
        """
        return self.user.first_name

    def last_name(self):
        """
        Proxy to main user model needed for admin
        """
        return self.user.last_name

    def __unicode__(self):
        return '{0}, ({1})'.format(
            self.user.username, self.user.get_full_name())
