__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '1/26/17'

from django.contrib.gis.db import models
#for user id foreign keys
from django.conf import settings
from django.contrib.auth.models import User

class Contact(models.Model):
    """
    Contact can be added by Admin
    """

    people_earth_obeservation = models.CharField('Person in charge for Earth Observation', max_length=255)
    email_earth_observation = models.CharField('Email for Earth Observation', max_length=255)
    phone_earth_observation = models.CharField('Phone for Earth Observation', max_length=255)
    catalogue_email_enqueries = models.CharField('Catalogue Email for Enqueries', max_length=255)
    catalogue_phone = models.CharField('Catalogue Telphone for Enqueries', max_length=255)

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

class Slider(models.Model):
    """
    To add image sliders in the home page. Only five slide
    """
    name = models.CharField('Slide Name', max_length=255)
    slide = models.ImageField(
        upload_to='images/slider/',
        blank=True,
        null=True)
