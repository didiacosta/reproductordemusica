# Generated by Django 2.2.10 on 2020-11-23 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_auto_20201123_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='caratula',
            field=models.ImageField(upload_to='al  bum'),
        ),
    ]
