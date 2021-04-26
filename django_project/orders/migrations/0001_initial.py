# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionaries', '0001_initial'),
        ('exchange', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Datums',
                'verbose_name_plural': 'Datums',
            },
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Delivery Method',
                'verbose_name_plural': 'Delivery Methods',
            },
        ),
        migrations.CreateModel(
            name='FileFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'File Format',
                'verbose_name_plural': 'File Formats',
            },
        ),
        migrations.CreateModel(
            name='MarketSector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='NonSearchRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_description', models.CharField(help_text=b'Description of an ordered product', max_length=100)),
                ('download_path', models.CharField(help_text=b'This is the location from where the product can be downloaded after a successfull OS4EO order placement.', max_length=512)),
                ('cost_per_scene', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('rand_cost_per_scene', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('currency', models.ForeignKey(blank=True, to='exchange.Currency', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(help_text=b'Make a note of any special requirements or processing instructions (including processing levels). Please note that in the case of free products and priority products, they will only be supplied with default options.', null=True, blank=True)),
                ('order_date', models.DateTimeField(help_text=b'When the order was placed - not shown to users', verbose_name=b'Order Date', auto_now_add=True)),
                ('datum', models.ForeignKey(default=1, verbose_name=b'Datum', to='orders.Datum')),
                ('delivery_method', models.ForeignKey(default=1, verbose_name=b'Delivery Method', to='orders.DeliveryMethod')),
                ('file_format', models.ForeignKey(default=1, verbose_name=b'File Format', to='orders.FileFormat')),
                ('market_sector', models.ForeignKey(default=1, to='orders.MarketSector')),
            ],
            options={
                'ordering': ['-order_date'],
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderNotificationRecipients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classes', models.ManyToManyField(help_text=b'Please subscribe to one or more product class. Use ctrl-click to select more than one.', to='contenttypes.ContentType', null=True, verbose_name=b'Product classes', blank=True)),
                ('satellite_instrument_group', models.ManyToManyField(help_text=b'Please choose one or more SatelliteInstrument. Use ctrl-clickto select more than one.', to='dictionaries.SatelliteInstrumentGroup', null=True, verbose_name=b'SatelliteInstrument', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Order Notification Recipient',
                'verbose_name_plural': 'Order Notification Recipients',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Order Status',
                'verbose_name_plural': 'Order Status List',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_change_date', models.DateTimeField(help_text=b'When the order status was changed', verbose_name=b'Date', auto_now_add=True)),
                ('notes', models.TextField()),
                ('new_order_status', models.ForeignKey(related_name='new_order_status', verbose_name=b'New Order Status', to='orders.OrderStatus')),
                ('old_order_status', models.ForeignKey(related_name='old_order_status', verbose_name=b'Old Order Status', to='orders.OrderStatus')),
                ('order', models.ForeignKey(to='orders.Order')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-order_change_date',),
                'verbose_name': 'Order Status History',
                'verbose_name_plural': 'Order Status History',
            },
        ),
        migrations.CreateModel(
            name='ResamplingMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Resampling Method',
                'verbose_name_plural': 'Resampling Methods',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(default=1, verbose_name=b'Order Status', to='orders.OrderStatus'),
        ),
        migrations.AddField(
            model_name='order',
            name='resampling_method',
            field=models.ForeignKey(default=2, verbose_name=b'Resampling Method', to='orders.ResamplingMethod'),
        ),
        migrations.AddField(
            model_name='order',
            name='subsidy_type_assigned',
            field=models.ForeignKey(related_name='subsidy_type+', blank=True, to='dictionaries.SubsidyType', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='subsidy_type_requested',
            field=models.ForeignKey(related_name='subsidy_type+', blank=True, to='dictionaries.SubsidyType', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nonsearchrecord',
            name='order',
            field=models.ForeignKey(blank=True, to='orders.Order', null=True),
        ),
        migrations.AddField(
            model_name='nonsearchrecord',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
