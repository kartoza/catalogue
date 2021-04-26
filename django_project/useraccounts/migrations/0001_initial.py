# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings
import easy_thumbnails.fields
import userena.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SansaUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'closed', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('strategic_partner', models.BooleanField(default=False, help_text=b'Mark this as true if the person belongs to an institution that is a CSIR/SAC strategic partner', verbose_name=b'Strategic Partner?')),
                ('url', models.URLField(blank=True)),
                ('about', models.TextField(blank=True)),
                ('address1', models.CharField(max_length=255, verbose_name=b'Address 1 (required)')),
                ('address2', models.CharField(max_length=255, verbose_name=b'Address 2 (required)')),
                ('address3', models.CharField(max_length=255, blank=True)),
                ('address4', models.CharField(max_length=255, blank=True)),
                ('post_code', models.CharField(max_length=25, verbose_name=b'Post Code (required)')),
                ('organisation', models.CharField(max_length=255, verbose_name=b'Organisation (required)')),
                ('contact_no', models.CharField(max_length=16, verbose_name=b'Contact No (required)')),
                ('user', models.OneToOneField(related_name='sansauserprofile', verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
    ]
