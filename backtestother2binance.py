from binance.client import Client
import pandas as pd
import talib
import math
import time
import traceback
import datetime
import json
import requests
from urllib.parse import urljoin
from datetime import datetime

# API_KEY = "199c420078b950fc6b4e9c42d5083fe5cde27fdf14b52c5a94a2f3a37f153fd2"
# API_SECRET = "d74500f1eafc05175b83cbc9d31ecad4ae1af259982661e8538bc9a5983f610c"

API_KEY = "B4zR8xuEb19jug5vwrDEmjqhmZrAgHcKxJ7ZHxv3E7896Zy48rzfHDuwwfCBKK8z"
API_SECRET = "wDJwThdEK0V5Y6SQ6ubTlV1RcbRvpzTWOhNBbPEnn4I7Qg6Rv2affNMlNWwJLsNr"

client = Client(API_KEY, API_SECRET, tld='com', testnet=False)

#----------------------------PreCondiciones-----------------------------------
encontrado = False
saldoinicial = 30.00
saldo = saldoinicial
saldo1 = saldoinicial
saldoEntrada = 0.00
apalancamiento = 1
comision = 0.0004
posicion = 0.00
#TipoOperacion = ""
#lost = 0.00000
#gain = 0.00000

symbol = 'BTCUSDT'
start_date = '2023-04-01 00:00:00'
end_date = '2023-04-30 00:00:00'

"""
date_format = '%Y-%m-%d %H:%M:%S'
start = datetime.strptime(start_date, date_format)
end = datetime.strptime(end_date, date_format)
difference = end - start
minutes = int(difference.total_seconds() / 60)
"""

intervalo = '1m'
numero = -30
numero2 = 0
numero3 = 0
numero4 = -30
def obtener_klines_formateado(simbolo, str_inicio, str_final, vela, dataframe = True, url_base = "https://fapi.binance.com/"):
    
    def timestamp_ms_to_datetime_str(timestamp_ms):
        return datetime.fromtimestamp(timestamp_ms/1000).strftime("%Y-%m-%d %H:%M:%S")
    
    timestamp_inicio = datetime.strptime(str_inicio, "%Y-%m-%d %H:%M:%S").timestamp()
    timestamp_final = datetime.strptime(str_final, "%Y-%m-%d %H:%M:%S").timestamp()
    
    timestamp_inicio = int(timestamp_inicio*1000) #en ms
    timestamp_final = int(timestamp_final*1000) #en ms
            
    try:
        path = '/fapi/v1/klines'
        
        parametros = {
            'symbol': simbolo,
            'interval': vela,
            'startTime': timestamp_inicio,
            'endTime': timestamp_final,
            'limit': 1440
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


posicion = False
otro = False
otro2 = False

profitM = 0.00
entrada = 0.
salida = 0.00

gananciasi = 0.00
perdidasi = 0.00
ganancias = 0.00
perdidas = 0.00
operacionT = 0
operaciones = 0
profit = 0.00

#-----------------------------Funciones------------------------------------
def abrir_operacion(precio):

	global saldo
	global apalancamiento
	global comision
	global posicion

	posicion = apalancamiento*saldo/precio
	posicion -= posicion*comision

def cerrar_operacion_long(precio):

    global saldo
    global apalancamiento
    global comision
    global posicion
    

    posicion *= precio
    posicion -= posicion*comision
    saldo = posicion - (apalancamiento*saldo - saldo)


def cerrar_operacion_short(precioapertura,preciofinal):

    global saldo
    global apalancamiento
    global comision
    global posicion
        
    price = precioapertura + (precioapertura - preciofinal)
    posicion *= price
    posicion -= posicion*comision
    saldo = posicion - (apalancamiento*saldo - saldo)

def macdprueba (num1,num2,num3,num4, macd, closes):
	
	global saldoEntrada
	global FechaApertura

	posicion = False
	otro = False
	otro2 = False

	profitM = 0.00
	entrada = 0.00
	salida = 0.00

	numero = float(num1)
	numero2 = float(num2)
	numero3 = float(num3)
	numero4 = float(num4)

	ganancias = 0.00
	perdidas = 0.00
	operacionT = 0

	gananciasi = 0.00
	perdidasi= 0.00
	precio_inicial = 0.00
	precio_cierre = 0.00
	operaciones = 0
	profit = 0.00
	i = 0

	for i in range(33,len(macd)):

		#print(histograma_minutely[i], " ", closes[i])

		#************************  LONG *****************************************			
		if  macd[i] < numero and posicion == False:
			
			TipoOperacion = "LONG"
			operaciones += 1
			posicion = True
			otro = True
			precio_inicial = closes[i]
			saldoEntrada = saldo
			abrir_operacion(precio_inicial)
			

			fecha_entrada = FechaApertura[i]


		if  macd[i] > numero2 and posicion == True and otro == True:

			precio_cierre = closes[i]
			posicion = False
			otro = False
			cerrar_operacion_long(precio_cierre)
			if precio_cierre > precio_inicial:
				gananciasi += saldo - saldoEntrada
			else:
				perdidasi +=saldo - saldoEntrada

				#print(f"{TipoOperacion}, apertura: {precio_inicial} - cierre {precio_cierre}, diferencia: {precio_cierre-precio_inicial}")

				if saldo <= 0:
					print("liquidacion")
					print(f"con {numero} y {numero2}")
					print(f"de {precio_inicial} a {precio_cierre}")

			fecha_salida = FechaApertura[i]
			print(f"{TipoOperacion}, resultado: {saldo-saldoEntrada}, {precio_inicial} - {precio_cierre}, diferencia {(((precio_cierre-precio_inicial)/precio_inicial)*100):.2f}, Fecha: {fecha_entrada} || {fecha_salida}")

# ***************************   SHORT *************************************************

		if macd[i] > numero3 and posicion == False:
			
			TipoOperacion = "SHORT"
			operaciones += 1
			posicion = True
			otro2 = True
			precio_inicial = closes[i]
			saldoEntrada = saldo
			abrir_operacion(precio_inicial)
			fecha_entrada = FechaApertura[i]

		if  macd[i] < numero4 and posicion == True and otro2 == True:
				
			precio_cierre = closes[i]
			posicion = False
			otro2 = False
			cerrar_operacion_short(precio_inicial, precio_cierre)
			if precio_inicial > precio_cierre:
				gananciasi += saldoEntrada - saldo

			else:
				perdidasi += saldoEntrada - saldo

				#print(f"{TipoOperacion}, apertura: {precio_inicial} - cierre {precio_cierre}, diferencia: {precio_cierre-precio_inicial}")

				if saldo <= 0:
					print("liquidacion")
					print(f"con {numero} y {numero2}")
					print(f"de {precio_inicial} a {precio_cierre}")

			fecha_salida = FechaApertura[i]
			print(f"{TipoOperacion}, resultado: {saldo-saldoEntrada}, {precio_inicial} - {precio_cierre}, diferencia {(((precio_inicial-precio_cierre)/precio_inicial)*100):.2f}, Fecha: {fecha_entrada} || {fecha_salida}")


	if posicion == True:
		operaciones -= 1

	ganancias = gananciasi
	perdidas = perdidasi
	operacionT = operaciones

	return ganancias, perdidas, operacionT
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

if __name__ == '__main__':


	posicion = 0.00
	saldo = saldoinicial

	inicio = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
	final = inicio + datetime.timedelta(days=1)
	profits = []
	profitR = 0.00
	
	# Iterar sobre los días de noviembre
	while inicio < datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'):
		
		finicio = inicio.strftime(date_format)
		ffinal = final.strftime(date_format)
		klines = obtener_klines_formateado(simbolo=symbol, 
	                                   str_inicio=finicio, 
	                                   str_final=ffinal, 
	                                   vela = intervalo,
	                                   dataframe = True)

		macd, _, _ = talib.MACD(klines['close'], fastperiod=12, slowperiod=26, signalperiod=9)


		FechaApertura = klines['open_datetime_str'] 

		closes = [float(valor) for valor in klines['close']]

		macd = [float(valor) for valor in macd]

		gananciasi, perdidasi, operaciones = macdprueba(numero, numero2, numero3, numero4, macd, closes)
		
	saldo1 = saldo
	entrada = numero
	salida = numero2
	ganancias = gananciasi
	perdidas = perdidasi
	operacionT = operaciones
	encontrado = True

	#*************************************************************************************

	print()
	print("*******************************************")
	print("El que mejor resultado tuvo fue")
	print(f"  en {operacionT} operaciones")
	total = ganancias + (perdidas*-1)
	if total == 0.00:
		total = 1
	print(f"positivos: {ganancias:.2f}$ : {(ganancias*100)/total:.2f}%")
	print(f"negativos: {perdidas:.2f}$ : {(perdidas*100)/total:.2f}%")
	print(f"***************\n {saldoinicial}$ se transformaron en {saldo1:.2f}$")
	print(f"profit: {((saldo1-saldoinicial)*100)/saldoinicial:.2f}%")
