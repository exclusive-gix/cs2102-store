# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def seed_multimedia(apps, schema_editor):
    call_command('loaddata', 'multimedia_data', app_label='multimedia')
    call_command('loaddata', 'multimediaimage_data', app_label='multimedia')

def delete_multimedia(apps, schema_editor):
    Book = apps.get_model('multimedia', 'Book')
    Music = apps.get_model('multimedia', 'Music')
    Album = apps.get_model('multimedia', 'Album')
    AlbumMusic = apps.get_model('multimedia', 'AlbumMusic')
    Movie = apps.get_model('multimedia', 'Movie')
    Application = apps.get_model('multimedia', 'Application')
    Multimedia = apps.get_model('multimedia', 'Multimedia')
    Organisation = apps.get_model('multimedia', 'Organisation')
    Category = apps.get_model('multimedia', 'Category')
    MultimediaCategory = apps.get_model('multimedia', 'MultimediaCategory')

    AlbumMusic.objects.all().delete()
    MultimediaCategory.objects.all().delete()
    Category.objects.all().delete()
    Book.objects.all().delete()
    Music.objects.all().delete()
    Album.objects.all().delete()
    Movie.objects.all().delete()
    Application.objects.all().delete()
    Multimedia.objects.all().delete()
    Organisation.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_create_model'),
    ]

    operations = [
        migrations.RunPython(
            seed_multimedia,
            delete_multimedia,
        ),
    ]
