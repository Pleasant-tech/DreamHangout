# Generated by Django 3.0.7 on 2020-08-02 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0036_auto_20200802_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
