# Generated by Django 2.1.7 on 2019-02-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
