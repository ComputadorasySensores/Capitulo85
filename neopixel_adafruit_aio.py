from machine import Pin
from neopixel import NeoPixel
import time
import network
import urequests as requests
import ujson
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("nombre_de_tu_red","contraseña_de_tu_red")

aio_key = "Tu_Active_Key"
username = "Tu_username"
encabezado = {'X-AIO-Key': aio_key, 'Content-Type': 'application/json'}

np = NeoPixel(Pin(28), 8)
feed_nombres = ['rojo', 'verde', 'azul']
rgb_valores = {'rojo': 0, 'verde': 0, 'azul': 0}
      
espera = 10
while espera > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    espera -= 1
    print('esperando conexión...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Error de conexión WiFi')
else:
    print('conectado')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    
def crear_URL(nombre_feed):
    url = "https://io.adafruit.com/api/v2/" + username + "/feeds/" + nombre_feed + "/data/last"
    return url
 
try:
    while True:
        for color in feed_nombres:
            respuesta = requests.get(crear_URL(color), headers=encabezado)
            parsed = ujson.loads(respuesta.text)
            valor = int(parsed['value'])
            rgb_valores[color] = valor
            print(valor)
        for i in range(8):
            np[i] = (rgb_valores['rojo'], rgb_valores['verde'], rgb_valores['azul'])
            np.write()
except KeyboardInterrupt:
    for i in range(8):
        np[i] = (0, 0, 0)
        np.write()
        time.sleep(0.5)
