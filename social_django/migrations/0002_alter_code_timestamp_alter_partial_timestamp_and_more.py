# Generated by Django 4.2.7 on 2025-01-23 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2025, 1, 23, 19, 52, 34, 284857)),
        ),
        migrations.AlterField(
            model_name='partial',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2025, 1, 23, 19, 52, 34, 285145)),
        ),
        migrations.AlterField(
            model_name='usersocialauth',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 23, 19, 52, 34, 283435)),
        ),
    ]
