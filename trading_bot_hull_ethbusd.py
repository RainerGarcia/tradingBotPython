from binance.client import Client
import pandas as pd
from os import system
import time
import talib
import threading
import traceback
import datetime
import json
import requests
from urllib.parse import urljoin
import keyboard
import numpy as np
import colorama
from colorama import Fore
from simulador_wallet import simulador_wallet
PAUSE = True

def pausar():
    global PAUSE
    while PAUSE:
        if keyboard.is_pressed('p'):
            PAUSE = False

def weighted_moving_average(data, window):
    weights = np.arange(1, window + 1)
    wma = np.convolve(data, weights[::-1], 'valid') / weights.sum()
    return wma

def hull_moving_average(data: list[float], length: int) -> list[float]:
    half_length = int(length/2)
    
    # Calcula las medias móviles ponderadas:
    first_wma = weighted_moving_average(data,length)
    second_wma = 2*weighted_moving_average(weighted_moving_average(data,half_length),half_length)[:len(first_wma)]

    diff_wmas=second_wma-first_wma
   
    #Calcula raiz cuadrado del periodo 
    sqrtLength=int(np.sqrt(length))
    
    # Ahora calculamos el HMA aplicando una WMA al resultado anterior.
    hull_ma=weighted_moving_average(diff_wmas,sqrtLength)

    return hull_ma

def obtener_klines_formateado(simbolo, dataframe = True, url_base = "https://fapi.binance.com/"):
    
    def timestamp_ms_to_datetime_str(timestamp_ms):
        return datetime.datetime.fromtimestamp(timestamp_ms/1000).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        path = '/fapi/v1/klines'
        
        parametros = {
            'symbol': simbolo,
            'interval': '1m',
            'limit': 68
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
        return data_klines_df
    else:
        return data_klines


def calculo_datos():
    klines = obtener_klines_formateado(simbolo='ETHBUSD',dataframe = True)
    FechaApertura = klines['open_datetime_str'] 
    closes = klines['close']
    return closes, FechaApertura


if __name__ == "__main__":

    operacion_long = False
    operacion_short = False
    operacion_abierta = False
    saldoinicial = 15.00
    profitDia = 0.00
    profits = []
    negativos = 0
    positivos = 0
    porcentajeloss = -0.50
    stoplossLONG = 1000000.00
    stoplossSHORT = -1000000.00
    liquidacion = 0.00

    hilo = threading.Thread(target=pausar)
    hilo.start()

    wallet = simulador_wallet(15.00, float(1))
    while PAUSE:
        close, FechaApertura = calculo_datos()
        HULL = hull_moving_average(close, int(55 * 1))
        hullColor = np.where(HULL > HULL[-2], "verde", "rojo") 
        #system('cls')
        print(len(close), len(hullColor))
        input()
        #print(closes[67],hullColor[1])

        color = hullColor[0]

        if hullColor[1] != color:

            color = "listo"

            if wallet.saldo <= 10.00:
                print("se perdio todo el dinero")
                break


            if hullColor[1] == "verde" and operacion_long == False and operacion_abierta == False:
                wallet.abrir_operacion(close[67])
                print("abrir operacion LONG")
                operacion_long = True
                operacion_abierta = True
                saldoEntrada = wallet.saldo
                precio_inicial = float(close[67])
                fecha_entrada = FechaApertura[67]
                stoplossLONG = ((precio_inicial*porcentajeloss)/100.00)+precio_inicial
                liquidacion = (((saldoEntrada*apalancado)-saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)
                
            
            if operacion_long == True and operacion_abierta == True:

                if close[67] <= liquidacion:
                    print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                if hullColor[1] == "rojo" or close[67] <= stoplossLONG:
                    wallet.cerrar_operacion_long(close[i])
                    operacion_long = False
                    operacion_abierta = False
                    print(f"LONG, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[67]}, diferencia {(((close[67]-precio_inicial)/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[67]}")
                    print()
                    profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                    profits.append(profitDia)
                    stoplossLONG = 1000000.00
                    saldoinicial = wallet.saldo
                    if (wallet.saldo-saldoEntrada) < 0:
                        negativos += 1
                    else:
                        positivos += 1

            if hullColor[1] == "rojo" and operacion_short == False and operacion_abierta == False:

                wallet.abrir_operacion(close[67])
                print("Abrir operacion SHORT")
                precioapertura = close[67]
                operacion_short = True
                operacion_abierta = True
                saldoEntrada = wallet.saldo
                precio_inicial = float(close[67])
                fecha_entrada = FechaApertura[67]
                stoplossSHORT = -(((precio_inicial*porcentajeloss)/100.00)-precio_inicial)
                liquidacion = (((saldoEntrada*apalancado)+saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)

            if  operacion_short == True and operacion_abierta == True:

                if close[67] >= liquidacion:
                    print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                if hullColor[1] == "verde" or close[67] >= stoplossSHORT:

                    wallet.cerrar_operacion_short(precioapertura, close[67])
                    operacion_short = False
                    operacion_abierta = False
                    print(f"SHORT, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[67]}, diferencia {(((precio_inicial-close[67])/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[67]}")
                    print()
                    profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                    profits.append(profitDia)
                    stoplossSHORT = -1000000.00
                    saldoinicial = wallet.saldo
                    if (wallet.saldo-saldoEntrada) < 0:
                        negativos += 1
                    else:
                        positivos += 1

    hilo.join()
    print(wallet.saldoinicial,"|--|",wallet.saldo)
    print("positivos: ", positivos ,"\negativos: ", negativos)
    print(f"profit: {sum(profits)/float(len(profits)):.2f}%")
    exit()

#hullcolor o el hull me elimina 66 datos, requiere al menos 67 datos de closes