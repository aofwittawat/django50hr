# Generated by Django 3.0 on 2021-04-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20210402_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpending',
            name='trackingnumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
