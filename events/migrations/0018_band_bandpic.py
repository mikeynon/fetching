# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-23 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20180223_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='bandpic',
            field=models.FileField(default=None, upload_to='static/images'),
            preserve_default=False,
        ),
    ]
