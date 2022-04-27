# Generated by Django 4.0.1 on 2022-03-19 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='licenseholder',
            name='Phone_num',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='licenseholder',
            name='validity',
            field=models.DateField(default=datetime.date(2022, 3, 20)),
        ),
        migrations.AddField(
            model_name='user',
            name='Phone_num',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='user',
            name='Registered_date',
            field=models.DateField(default=datetime.date(2022, 3, 20)),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]