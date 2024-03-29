# import websocket
# import json
# import requests

# # Realizamos una solicitud GET a la API para obtener los últimos 100 precios
# url = "https://fapi.binance.com/fapi/v1/klines"
# params = {
#     "symbol": "BTCUSDT",
#     "interval": "1m",
#     "limit": 100
# }
# response = requests.get(url, params=params)
# data = response.json()

# # Imprimimos los precios históricos
# print("Precios históricos:")
# for d in data:
#     print(d[1])

# # Función que maneja el stream de datos en tiempo real
# def on_message(ws, message):
#     data = json.loads(message)
#     if data["e"] == "kline":
#         print("Nuevo precio:", data["k"]["c"])

from binance.client import Client
import pandas as pd
import numpy
import talib
import math
import time
import traceback
import datetime
import json
import requests
from urllib.parse import urljoin
import csv
import itertools

# API_KEY = "199c420078b950fc6b4e9c42d5083fe5cde27fdf14b52c5a94a2f3a37f153fd2"
# API_SECRET = "d74500f1eafc05175b83cbc9d31ecad4ae1af259982661e8538bc9a5983f610c"

# API_KEY = "B4zR8xuEb19jug5vwrDEmjqhmZrAgHcKxJ7ZHxv3E7896Zy48rzfHDuwwfCBKK8z"
# API_SECRET = "wDJwThdEK0V5Y6SQ6ubTlV1RcbRvpzTWOhNBbPEnn4I7Qg6Rv2affNMlNWwJLsNr"

# client = Client(API_KEY, API_SECRET, tld='com', testnet=False)

#----------------------------PreCondiciones-----------------------------------
encontrado = False
saldoinicial = 30.00
saldo = saldoinicial
saldo1 = saldoinicial
saldoinicial1 = saldoinicial
saldoEntrada = 0.00
apalancamiento = 1
comision = 0.0004
posicion = 0.00
intervaloR = ''
#TipoOperacion = ""
#lost = 0.00000
#gain = 0.00000

symbol = 'BTCUSDT'
start_date = '2023-05-01 00:00:00'
end_date = '2023-05-30 00:00:00'
#TipoOperacion = ''


def obtener_klines_formateado(simbolo, str_inicio, str_final, vela, dataframe = True, url_base = "https://fapi.binance.com/"):
    
    def timestamp_ms_to_datetime_str(timestamp_ms):
        return datetime.datetime.fromtimestamp(timestamp_ms/1000).strftime("%Y-%m-%d %H:%M:%S")
    
    timestamp_inicio = datetime.datetime.strptime(str_inicio, "%Y-%m-%d %H:%M:%S").timestamp()
    timestamp_final = datetime.datetime.strptime(str_final, "%Y-%m-%d %H:%M:%S").timestamp()
    
    timestamp_inicio = int(timestamp_inicio*1000) #en ms
    timestamp_final = int(timestamp_final*1000) #en ms
    
    if vela == '1m':
        limit = 1440
    elif vela == '3m':
        limit = 480
    elif vela == '5m':
        limit = 288
    elif vela == '15m':
        limit = 96
    elif vela == '30m':
        limit = 48
    try:
        path = '/fapi/v1/klines'
        
        parametros = {
            'symbol': simbolo,
            'interval': vela,
            'startTime': timestamp_inicio,
            'endTime': timestamp_final,
            'limit': limit
        }
        
        url = urljoin(url_base, path)
        r = requests.get(url, params=parametros)
        if r.status_code == 200:
            data_klines = r.json()
        else:
            print(f"Status code: {r.status_code}")
            print(r.json())
            raise Exception
    except:
        traceback.print_exc()
        data_klines = None
        
    for kline in data_klines:
        kline[1] = float(kline[1])
        kline[2] = float(kline[2])
        kline[3] = float(kline[3])
        kline[4] = float(kline[4])
        kline[5] = float(kline[5])
        kline[7] = float(kline[7])
        kline[9] = float(kline[9])
        kline[10] = float(kline[10])
        kline.insert(1, timestamp_ms_to_datetime_str(kline[0]))
        kline.insert(8, timestamp_ms_to_datetime_str(kline[7]))
        
    if dataframe:
        data_klines_df = pd.DataFrame(data_klines, columns=['timestamp', 'open_datetime_str', 'open', 'high', 'low', 'close', 'close_datetime_str', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']) 
        #data_klines_df['timestamp'] = pd.to_datetime(data_klines_df['timestamp'], unit='ms')
        return data_klines_df
    else:
        return data_klines


def calculo_datos(intervalo,fechainicio,fechafinal):
    klines = obtener_klines_formateado(simbolo=symbol, 
                                       str_inicio=fechainicio, 
                                       str_final=fechafinal, 
                                       vela = intervalo,
                                       dataframe = True)


    FechaApertura = klines['open_datetime_str'] 

    closes = klines['close']

    # for i in range(len(histograma)):
    #   print(histograma[i], FechaApertura[i], closes[i])
    # input()

    histograma_minutely = histograma

    return closes, histograma_minutely, FechaApertura

    # ver si con esto se puede modificar para que de los klines correctos actualizandose en tiempo real 