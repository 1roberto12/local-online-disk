# Generated by Django 2.1.4 on 2019-01-13 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190113_1306'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='shared_with_me',
            field=models.ManyToManyField(to='api.SharedFile'),
        ),
    ]
