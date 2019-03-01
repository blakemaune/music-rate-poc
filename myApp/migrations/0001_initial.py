# Generated by Django 2.1.7 on 2019-02-28 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('spotify_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('art_url', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
