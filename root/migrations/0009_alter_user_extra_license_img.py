# Generated by Django 4.0.1 on 2022-04-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0008_delete_user_1_user_extra_license_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_extra',
            name='License_img',
            field=models.ImageField(default='pics\\tempo.png', upload_to='pics'),
        ),
    ]
