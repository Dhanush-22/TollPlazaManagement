# Generated by Django 4.0.1 on 2022-04-23 06:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0009_alter_user_extra_license_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licenseholder',
            name='validity',
            field=models.DateField(default=datetime.date(2022, 4, 23)),
        ),
        migrations.AlterField(
            model_name='user_extra',
            name='License_img',
            field=models.ImageField(default='tempo.png', upload_to=''),
        ),
    ]
