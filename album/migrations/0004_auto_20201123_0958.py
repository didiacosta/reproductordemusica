# Generated by Django 2.2.10 on 2020-11-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20201123_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='caratula',
            field=models.ImageField(upload_to='album'),
        ),
    ]
