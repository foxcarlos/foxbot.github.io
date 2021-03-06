#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django
from django.db import models
from datetime import timedelta, datetime
from random import randint

# Create your models here.

class BlackList(models.Model):
    '''.'''

    mencion = models.CharField(max_length=100, blank=False, null=False,
            unique=True)
    activo = models.BooleanField(default=False)


class User(models.Model):
    '''.'''

    chat_id = models.IntegerField(default=0)
    username = models.CharField(max_length=50, blank=True, null=True,)
    first_name = models.CharField(max_length=50, blank=True, null=True,)
    last_name = models.CharField(max_length=50, blank=True, null=True,)
    language_code = models.CharField(max_length=50, blank=True, null=True,)

    def __str__(self):
        return u'{0}-{1}'.format(self.first_name, self.username)

    class Meta:
        '''.'''
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['username']


class Grupo(models.Model):
    grupo_id = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=200, default="Sin Descripcion", blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        #return str(self.grupo_id)
        return self.descripcion if self.descripcion else 'Sin descripcion'

    class Meta:
        '''.'''
        verbose_name_plural = 'Grupos'
        verbose_name = 'Grupo'
        ordering = ['descripcion']

    def buscar_o_crear(grupo_chat_id, grupo_descripcion, grupo_tipo):
        grupo = Grupo.objects.update_or_create(grupo_id=grupo_chat_id)[0]
        grupo.descripcion = grupo_descripcion
        grupo.tipo = grupo_tipo
        grupo.save()
        return grupo


class Comando(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre


class ComandoEstado(models.Model):
    grupo_id = models.IntegerField(default=0)
    comando = models.ForeignKey(Comando, related_name='Comandos', on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    chat_id = models.IntegerField(default=0)


class Alerta(models.Model):
    '''.'''
    comando = models.CharField(max_length=100, blank=True, null=True, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=False)
    # ultimo_precio = models.FloatField(default=0.0)

    def __str__(self):
        return self.comando

    class Meta:
        '''.'''
        verbose_name_plural = 'Alertas'
        verbose_name = 'Alerta'
        ordering = ['comando']


class AlertaUsuario(models.Model):
    '''.'''
    alerta = models.ForeignKey(Alerta, related_name='alertas', on_delete=models.CASCADE)
    estado = models.CharField(max_length=3, default="I",\
            choices=(
                ('A', 'On'),
                ('I', 'Off')
                ),)

    chat_id = models.IntegerField(blank=True, null=False)
    chat_username = models.CharField(max_length=100, blank=True, null=True)
    frecuencia = models.IntegerField(default=120,
            verbose_name="frecuencia de notificacion de alertas en minutos",
            help_text="Tiempo en segundos")
    porcentaje_cambio = models.IntegerField(default=0,
            verbose_name="Porcentaje de cambio en la tasa",
            help_text="Numero entero")
    ultima_actualizacion = models.DateTimeField(default=django.utils.timezone.now(), blank=True, null=True)
    ultimo_precio = models.FloatField(default=0.0)

    def __str__(self):
        return self.alerta.comando

    class Meta:
        '''.'''
        verbose_name_plural = 'AlertasUsuarios'
        verbose_name = 'AlertaUsuario'
        ordering = ['alerta']


class Contrato(models.Model):
    '''.'''

    contrato = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    operacion = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.contrato

    class Meta:
        '''.'''
        verbose_name_plural = 'Contratos'
        verbose_name = 'Contrato'
        ordering = ['fecha']

    def generar_nro_contrato():
        contrato_nro = str(int(randint(0,9796220)+datetime.timestamp(datetime.now())))
        return contrato_nro


class PersonaContrato(models.Model):
    '''.'''

    contrato = models.ForeignKey(Contrato, related_name="contratos", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    tipo_buyer_seller = models.CharField(max_length=50, blank=True, null=True)
    puntuacion = models.CharField(max_length=15, default="neu",
            choices=(
                ("pos", "Positivo"),
                ("neg", "Negativo"),
                ("neu", "Neutral")))
    comentario = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.contrato)

