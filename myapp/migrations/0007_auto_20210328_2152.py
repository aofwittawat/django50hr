# Generated by Django 3.0 on 2021-03-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='defaultprofile.jpg', null=True, upload_to='photoprofile'),
        ),
    ]
