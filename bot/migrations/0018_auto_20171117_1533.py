# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 15:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0017_auto_20171116_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertausuario',
            name='ultima_actualizacion',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 17, 15, 33, 19, 475147), null=True),
        ),
    ]