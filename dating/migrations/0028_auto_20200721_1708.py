# Generated by Django 3.0.7 on 2020-07-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0027_remove_thread_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='value',
            field=models.CharField(default='', max_length=200),
        ),
    ]
