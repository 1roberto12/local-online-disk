# Generated by Django 2.1.4 on 2019-01-14 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190114_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedfile',
            name='filename',
        ),
    ]
