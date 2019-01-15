# Generated by Django 2.1.4 on 2019-01-14 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190113_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedfile',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharedfile',
            name='path',
            field=models.CharField(max_length=255),
        ),
    ]