# Generated by Django 4.2.6 on 2024-02-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_useraccount_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pictures/'),
        ),
    ]
