# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_user_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alerta',
            name='ultimo_precio',
        ),
        migrations.AddField(
            model_name='alertausuario',
            name='ultimo_precio',
            field=models.FloatField(default=0.0),
        ),
    ]