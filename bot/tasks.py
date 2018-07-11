# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

import requests
from lxml import html
from time import sleep
from pytube import YouTube
import os
from datetime import datetime
import urllib.request as urllib2
import urllib
from emoji import emojize
from bs4 import BeautifulSoup
import tweepy

from django_telegrambot.apps import DjangoTelegramBot
from sampleproject.celery import app

from django.conf import settings
# celery -A pyloro worker -l info


from lib.airtm import AirTM


URL_AREPA_BTC_USD = settings.CRIPTO_MONEDAS.get("URL_AREPACOIN")


@app.task
def pool_message(users, cadena_sin_el_comando):
    for user in users if cadena_sin_el_comando else []:
        try:
            # DjangoTelegramBot.dispatcher.bot.sendMessage(user.get("chat_id"), text=cadena_sin_el_comando)
            print(user.get("chat_id ", cadena_sin_el_comando))
        except Exception as E:
            print(E)
        sleep(3)


@app.task
def grupo_message(grupos, cadena_sin_el_comando):
    for grupo in grupos if cadena_sin_el_comando else []:
        try:
            # DjangoTelegramBot.dispatcher.bot.sendMessage(grupo.get("grupo_id"), text=cadena_sin_el_comando)
            print(grupo.get("grupo_id ", cadena_sin_el_comando))
        except Exception as E:
            print(E)
        sleep(3)


@app.task
def yt2mp3(chat_id, url):
    msg_response = []

    def convert_to_mp3(stream, file_handle):
        import os
        import re
        try:
            nombre = os.path.split(os.path.abspath(file_handle.name))[1]
            print('Nombre', nombre)
            filename = nombre.replace(" ", "_").replace("mp4", "")
            filename_2 = ''.join(re.findall('\w', filename))
            filename_mp3 = "{0}.mp3".format(filename_2)
            comando = 'ffmpeg -i "{0}" -vn -ar 44100 -ac 2 -ab 192 -f mp3 {1}'.format(nombre, filename_mp3)
            print(comando)
            os.system(comando)
            msg_response.append("{0}".format(filename_mp3))
            os.remove(nombre)
        except Exception as E:
            print('error', E)
            os.remove(nombre)
            msg_response.append(":x: <b>Ocurrio un error al procesar el arachivo</b>")
        return msg_response

    try:
        yt = YouTube(url)
        yt.register_on_complete_callback(convert_to_mp3)
        yt.streams.filter(only_audio=True).first().download()

        archivo = msg_response[0]
        file_ = open("{0}".format(archivo), "rb")
        DjangoTelegramBot.dispatcher.bot.sendAudio(chat_id,
                audio=file_, caption=archivo)

        file_.close()
        os.remove(archivo)
    except Exception as E:
        print(E)


def api_tuiter():
    consumer_key = "wz6LRrWGEj0cfOsSqNKLg"
    consumer_secret = "JQUF9IFiFOpzjpTKYxsbKl5QV6o0baoD37fxFpBEE"
    access_token = "23130430-jfgPU8pnQks4AuW5XpS9Wfg3IaYMd4jB88zw8nPm4"
    access_token_secret = "8q9haKn2GrtqDmqMjxRCH0x8UEst1Ckt33AsnJYk"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


# @app.task
def get_price_from_twiter(nombre):

    def _validar_condicion(usuario_tuiter, status):
        if usuario_tuiter == 'theairtm':
            if 'Tasa' in status.text and '#Ven' in status.text:
                return True
        elif usuario_tuiter == 'dolarprocom':
            if 'PRECIO DEL MERCADO PARALELO' in status.text:
                return True
        elif usuario_tuiter == 'MonitorDolarVe':
            if u'paralelo en Venezuela (en Bs.)' in status.text:
                return True
        else:
            return False
        return False

    def get_stuff(nombre=None):
        api = api_tuiter()
        stuff = tweepy.Cursor(api.user_timeline, screen_name=nombre, include_rts=True)
        return stuff

    def descargar_imagen(nombre, status):
        if _validar_condicion(nombre, status):
            response = ''
            media = status.entities.get('media')
            if media:
                url_imagen = media[0].get('media_url')
                if url_imagen:
                    ruta_imagen_tasa = 'graficos/tasa_{0}.jpg'.format(nombre)
                    # urllib2.urlretrieve(url_imagen, ruta_imagen_tasa)
                    response = ruta_imagen_tasa
            return response

    def get_tweets(stuff, n, nombre):
        for index, status in enumerate(stuff.items(n)):
            today = status.created_at.date()
            response_ruta = descargar_imagen(nombre, status)
            texto = status.text

            if response_ruta:
                if today == datetime.now().date():
                    response = True, response_ruta, texto
                    break
                else:
                    response = False, response_ruta, texto
                    break
            else:
                response = False, '', 'No disponible'
        return response

    def parsear_tasa(texto):
        response = ''
        texto_descomponer = texto.split() if len(texto.split()) >= 4 else ''
        if texto_descomponer:
            tasa = [float(palabra.replace(',', '')) for palabra in texto.split() if len(palabra) > 4 and palabra.replace(',', '').replace('.', '').isdigit()]
            # tasa = texto_descomponer[0] if texto_descomponer[0].lower() == 'tasa' or texto_descomponer[0].upper() == u'ACTUALIZACIÓN' else ''
            # moneda = texto_descomponer[3] if texto_descomponer[3].lower() == 'bsf' else ''
            moneda = 'tasa' in texto.lower() and 'bs' in texto.lower() and '#ven' in texto.lower()
            if tasa and moneda:
                response = str(tasa[0])
        return response

    stuff = get_stuff(nombre)
    hoy, ruta_img, texto = get_tweets(stuff, 50, nombre)
    return parsear_tasa(texto)


@app.task
def airtm_dolar_vef(chat_id):
    # instancia = AirTM()

    if not instancia.verificar_instancia_abierta():
        instancia.abrir_navegador()

    instancia.verfifica_login()
    sleep(5)
    dolar_airtm = instancia.obtener_precio()
    instancia.cerrar()
    print(dolar_airtm)

    if dolar_airtm:
        response = """El precio del Dolar AirTM es:\n\n\U0001F1FB\U0001F1EA <b>VEF:</b> {0:,.2f}""".format(dolar_airtm)
    else:
        response = ':x: <b>Error al consultar AirTM</b>'
    DjangoTelegramBot.dispatcher.bot.sendMessage(chat_id, parse_mode="html", text=emojize(response, use_aliases=True))

def get_dolar_gobierno():
    dolar_gobierno = ''
    URL = 'https://www.casadecambiozoom.com/'
    ruta ='/html/body/div[3]/div/div[2]/a/font'
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    resultado_bs = tree.xpath(ruta)
    if resultado_bs:
        dolar_gobierno = resultado_bs[0].text.replace('Bs.', '').strip()
    return dolar_gobierno

def get_price_arepacoin2(dolartoday):
    precio_dtd = dolartoday if dolartoday else 0
    precio_airtm = float(get_price_from_twiter('theairtm').strip()) if \
            get_price_from_twiter('theairtm') else 0
    dolartoday if dolartoday else 0

    precio_usd_arepa = 0
    precio_vef_arepa = 0
    precio_btc_arepa = 0
    precio_vef_arepa_airtm = 0

    URL = "https://coinlib.io/coin/AREPA/ArepaCoin"

    page = requests.get(URL)
    tree = html.fromstring(page.content)
    resultado_usd = tree.xpath('//*[@id="coin-main-price"]')
    resultado_btc = tree.xpath('//*[@id="altprice-859"]')

    if resultado_btc:
        precio_btc_arepa = float(resultado_btc[0].text.replace('BTC', '').strip())

    if resultado_usd:
        precio_usd_arepa = float(resultado_usd[0].text.replace(u'\xa0', '').replace(u'\n', '').replace('$', ''))

    precio_vef_arepa = precio_usd_arepa * precio_dtd
    precio_vef_arepa_airtm = precio_usd_arepa * precio_airtm

    return precio_usd_arepa, precio_vef_arepa, precio_vef_arepa_airtm, precio_btc_arepa

def get_price_wcc():

    vdisplay = Display(visible=0, size=(1024, 768))
    vdisplay.start()

    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
    url = "https://wolfclover.com/calculadora/"
    driver.get(url)

    wcc = driver.find_element_by_id("txt_clover")
    wcc.send_keys('1')

    tasa_dolar = driver.find_element_by_id("lbl_usdvef").text.replace('.', ',')
    btc = driver.find_element_by_id("txt_cryptocoin").get_attribute("value")
    vef = driver.find_element_by_id("txt_currency").get_attribute("value")
    usd = driver.find_element_by_id("txt_usd").get_attribute("value")

    vdisplay.stop()
    return tasa_dolar, vef, usd, btc

@app.task
def wolfclover(chat_id):

    tasa, vef, usd, btc = wcc()
    response = """El precio de WolfClover es:\n\n\<b>Tasa:</b>{0}\n
    U0001F1FB\U0001F1EA <b>VEF:</b> {1}\n\
    <b>:dollar: USD:</b> {2}\n\
    U000020BF <b>BTC</b> {3}\n""".format(tasa, vef, usd, btc)

    DjangoTelegramBot.dispatcher.bot.sendMessage(chat_id, parse_mode="html",
            text=emojize(response, use_aliases=True))

def get_price_arepacoin(dolartoday):
    precio_dtd = dolartoday if dolartoday else 0
    precio_airtm = float(get_price_from_twiter('theairtm').strip()) if \
            get_price_from_twiter('theairtm') else 0
    dolartoday if dolartoday else 0

    precio_usd_arepa = 0
    precio_vef_arepa = 0
    precio_btc_arepa = 0
    precio_vef_arepa_airtm = 0

    coincap_data = requests.get(URL_AREPA_BTC_USD).json()
    coincap_json = coincap_data.get('data') if \
            coincap_data.get('status') == 'success' else {}

    arepa_values = [coin for coin in coincap_json \
            if coin.get('name').lower() == 'arepacoin'][0]

    if arepa_values:
        precio_btc_arepa = arepa_values.get('price_btc')
        precio_usd_arepa = arepa_values.get('price_usd')

    precio_vef_arepa = precio_usd_arepa * precio_dtd
    precio_vef_arepa_airtm = precio_usd_arepa * precio_airtm

    return precio_usd_arepa, precio_vef_arepa, precio_vef_arepa_airtm, precio_btc_arepa

@app.task
def arepacoin(chat_id, dolartoday):
    precio_usd_arepa, precio_vef_arepa, precio_vef_arepa_airtm, precio_btc_arepa  = get_price_arepacoin(dolartoday)

    response = """El precio de ArepaCoin es:\n\n\U0001F1FB\U0001F1EA <b>VEF Dolartoday:</b> {0:,.2f}\n\U0001F1FB\U0001F1EA <b>VEF AirTM:</b> {2:,.2f}\n<b>:dollar: USD:</b> {1:,.8f}\n\U000020BF <b>BTC</b> {3:,.8f}\n""".format(precio_vef_arepa, precio_usd_arepa, precio_vef_arepa_airtm, precio_btc_arepa)

    DjangoTelegramBot.dispatcher.bot.sendMessage(chat_id, parse_mode="html", text=emojize(response, use_aliases=True))
