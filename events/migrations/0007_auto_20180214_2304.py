# Generated by Django 2.0 on 2018-02-14 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_bandpictures'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchbandsugg',
            old_name='searchBand',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='searchvenuesugg',
            old_name='searchVenue',
            new_name='name',
        ),
    ]
