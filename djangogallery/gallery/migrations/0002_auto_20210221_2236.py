# Generated by Django 3.1.7 on 2021-02-21 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 21, 22, 36, 56, 198062), verbose_name='Date added'),
        ),
    ]
