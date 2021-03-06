# Generated by Django 2.2.10 on 2020-11-22 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artista', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('caratula', models.ImageField(upload_to='album')),
                ('artista_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artista.Artista')),
            ],
            options={
                'db_table': 'album_album',
            },
        ),
    ]
