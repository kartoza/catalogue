# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20160415_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name=b'IP Address'),
        ),
    ]