# Generated by Django 3.1.7 on 2021-05-07 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0004_auto_20210421_0439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-pk', 'last_name', 'first_name']},
        ),
    ]