# Generated by Django 2.2.10 on 2020-11-23 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='artista_id',
            new_name='artista',
        ),
    ]
