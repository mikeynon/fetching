# Generated by Django 2.0 on 2018-02-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='BandPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picUrl', models.CharField(max_length=100)),
            ],
        ),
    ]
