# Generated by Django 4.0.3 on 2022-06-18 13:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project_procurements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 18, 13, 38, 42, 404124, tzinfo=utc)),
        ),
    ]
