# Generated by Django 3.1.7 on 2021-04-21 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20210421_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='void_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
