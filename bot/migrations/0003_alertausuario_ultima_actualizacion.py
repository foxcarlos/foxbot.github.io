# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alerta_ultimo_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertausuario',
            name='ultima_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
