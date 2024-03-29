from binance.client import Client
from binance.enums import *
import pandas as pd
import talib
import time
import threading
import math
import csv
import itertools
import datetime
#-----------------------------Binance Testnet-----------------------------------
API_KEY = ""
API_SECRET = ""

client = Client(API_KEY, API_SECRET, tld='com', testnet=True)
symbolTicker = 'BTCUSDT'

#precondicion
klines = client.futures_historical_klines(symbolTicker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")


precio= 0.00
histogram_last = 0.00

saldo = 10.00000
apalancamiento = saldo*1
comision = 0.0004
posicion = 0.00000000
perdidas = 0.00000
ganancias = 0.00000

#-------------------FUNCIONES------------------------------------------------------

def cal_macd():

    global histogram_last
    global klines
    
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')
    df = df.astype(float)

    _, _, histogram_last = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

def precio_actual():
    global precio
    global klines

    precio = float(klines[1][4])

def abrir_operacion():

    global precio
    global apalancamiento
    global comision
    global posicion

    posicion = apalancamiento/precio
    posicion -= posicion*comision

def cerrar_operacion_long():

    global precio
    global saldo
    global apalancamiento
    global comision
    global posicion
    

    posicion *= precio
    posicion -= posicion*comision
    saldo = posicion - (apalancamiento - saldo)

def cerrar_operacion_short(precioapertura,resultado):

    global saldo
    global apalancamiento
    global comision
    global posicion
        
    price = precioapertura + resultado
    posicion *= price
    posicion -= posicion*comision
    saldo = posicion - (apalancamiento - saldo)

if __name__== "__main__":

    cal_macd()
    precio_actual()

    print(histogram_last)
    print(precio)

"""

for i in range(,len(klines)):

    prom = sum / 20

    if ( float(klines[i][4]) < prom*0.99 and 0 <= q < 5):
        #compra
        #print("compra  " + str(klines[i][4]))
        q = q + 1
        cantCompra = cantCompra +1
        dineroFinal = dineroFinal - prom*0.99#*1.00075
        #time.sleep(1)
    if ( float(klines[i][4]) > prom*1.01 and 0 < q <= 5):
        #venta
        #print("venta  " + str(klines[i][4]))
        q = q - 1
        cantVenta = cantVenta +1
        dineroFinal = dineroFinal + prom*1.01#*0.99925
        #time.sleep(1)

print(dineroFinal)
print(cantCompra)
print(cantVenta)
"""
