# Generated by Django 3.0.5 on 2020-06-14 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0019_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
