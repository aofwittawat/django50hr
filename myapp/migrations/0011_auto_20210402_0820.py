# Generated by Django 3.0 on 2021-04-02 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20210401_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderlist',
            old_name='oderid',
            new_name='orderid',
        ),
        migrations.RenameField(
            model_name='orderpending',
            old_name='oderid',
            new_name='orderid',
        ),
    ]
