# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comando', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('activo', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['comando'],
                'verbose_name': 'Alerta',
                'verbose_name_plural': 'Alertas',
            },
        ),
        migrations.CreateModel(
            name='AlertaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('A', 'On'), ('I', 'Off')], default='Off', max_length=3)),
                ('chat_id', models.IntegerField(default=0)),
                ('chat_username', models.CharField(blank=True, max_length=100, null=True)),
                ('alerta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alertas', to='bot.Alerta')),
            ],
            options={
                'ordering': ['alerta'],
                'verbose_name': 'AlertaUsuario',
                'verbose_name_plural': 'AlertasUsuarios',
            },
        ),
    ]
