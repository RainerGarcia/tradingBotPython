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

# API_KEY = ""
# API_SECRET = ""

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

symbol = 'ETHUSDT'
start_date = '2021-01-01 00:00:00'
end_date = '2023-06-30 00:00:00'
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
	# 	print(histograma[i], FechaApertura[i], closes[i])
	# input()

	return closes, FechaApertura

posicion = False
otro = False
otro2 = False

profitM = 0.00
entrada = 0.00
salida = 0.00

numero = 0
numero2 = 0
gananciasi = 0.00
perdidasi = 0
perdidasT = 0
ganancias = 0.00
perdidas = 100
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
    saldo = posicion - ((apalancamiento*saldo) - saldo)


def cerrar_operacion_short(precioapertura,preciofinal):

    global saldo
    global apalancamiento
    global comision
    global posicion
        
    price = precioapertura + (precioapertura - preciofinal)
    posicion *= price
    posicion -= posicion*comision
    saldo = posicion - ((apalancamiento*saldo) - saldo)

def macdprueba (num1,num2, histograma_minutely, closes, FechaApertura):
	posicion = False
	otro = False
	otro2 = False
	saldoEntrada = 0.00
	global TipoOperacion
	global saldo
	global saldoinicial
	perdidasT = 0

	profitM = 0.00
	entrada = 0.00
	salida = 0.00

	numero = float(num1)
	numero2 = float(num2)

	ganancias = 0.00
	perdidas = 0
	operacionT = 0

	gananciasi = 0.00
	perdidasi= 0
	precio_inicial = 0.00
	precio_cierre = 0.00
	operaciones = 0
	profit = 0.00
	i = 0

	profits = []
	profitR = 0.00
	profitDia = 0.00
	perdidasi = 0
	perdidasT = 0
	operacionT = 0

	saldo = 30.00
	saldoinicial = saldo

	for i in range(33,len(histograma_minutely)):

		saldoinicial = saldo

		#************************  LONG *****************************************			

		if float(histograma_minutely[i]) < numero  and posicion == False:
			operaciones += 1
			posicion = True
			otro = True
			precio_inicial = closes[i]
			saldoEntrada = saldo
			abrir_operacion(precio_inicial)
			fecha_entrada = FechaApertura[i]


		if float(histograma_minutely[i]) > numero2 and posicion == True and otro == True:
			precio_cierre = closes[i]
			posicion = False
			otro = False
			cerrar_operacion_long(precio_cierre)
			fecha_salida = FechaApertura[i]

			result = ((precio_cierre-precio_inicial)/precio_inicial)*100
			if result < 0.00:
				perdidasT += 1
			#print(f"LONG, resultado: {saldo-saldoEntrada}, {precio_inicial} - {precio_cierre}, diferencia {(((precio_cierre-precio_inicial)/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {fecha_salida}")
			profitDia = ((saldo-saldoinicial)*100)/saldoinicial
			profits.append(profitDia)
			
			
# ***************************   SHORT *************************************************
		
		if float(histograma_minutely[i]) > numero2 and posicion == False:
			operaciones += 1
			posicion = True
			otro2 = True
			precio_inicial = closes[i]
			saldoEntrada = saldo
			abrir_operacion(precio_inicial)
			fecha_entrada = FechaApertura[i]
		if float(histograma_minutely[i]) < numero and posicion == True and otro2 == True:
				precio_cierre = closes[i]
				posicion = False
				otro2 = False
				cerrar_operacion_short(precio_inicial, precio_cierre)
				fecha_salida = FechaApertura[i]

				result = ((precio_inicial-precio_cierre)/precio_inicial)*100
				if result < 0.00:
					perdidasT += 1

				#print(f"SHORT, resultado: {saldo-saldoEntrada}, {precio_inicial} - {precio_cierre}, diferencia {(((precio_inicial-precio_cierre)/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {fecha_salida}")
				profitDia = ((saldo-saldoinicial)*100)/saldoinicial
				profits.append(profitDia)
		
		
		# print(finicio,"----",ffinal, ": ", profitDia,"\n")

		
		# 	inicio += datetime.timedelta(days=1)  # Suma un día a la fecha actual
		# 	final += datetime.timedelta(days=1)  # Suma un día a la fecha siguiente
		# 	operacionT += operaciones
		# 	perdidasT += perdidasi
	try:
		profitR = sum(profits)/float(len(profits))
	except:
		print()

	entrada = numero
	salida = numero2
	perdidas = perdidasT
	operacionT = operaciones

	return entrada, salida, perdidas, operacionT, profitR

def escribir_csv(closes,dia,fecha, intervalo):
	filas = zip(closes, dia)

	fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')

	año = "2021"
	mes = "ENERO"

	if fecha.year == 2022:
		año = "2022"
	elif fecha.year == 2023:
		año = "2023"

	if fecha.month == 2:
		mes = "FEBRERO"
	elif fecha.month == 3:
		mes = "MARZO"
	elif fecha.month == 4:
		mes = "ABRIL"
	elif fecha.month == 5:
		mes = "MAYO"
	elif fecha.month == 6:
		mes = "JUNIO"
	elif fecha.month == 7:
		mes = "JULIO"
	elif fecha.month == 8:
		mes = "AGOSTO"
	elif fecha.month == 9:
		mes = "SEPTIEMBRE"
	elif fecha.month == 10:
		mes = "OCTUBRE"
	elif fecha.month == 11:
		mes = "NOVIEMBRE"
	elif fecha.month == 12:
		mes = "DICIEMBRE"
		
	# Escribir las filas en un archivo CSV
	with open('datos_historicos_ETHUSDT/'+mes+'_'+año+'_'+intervalo+'.csv', mode='a', newline='') as f:
		writer = csv.writer(f)
		for fila in filas:
			writer.writerow(fila)

def leer_cal_datos(path,i,j,k):

	with open(path, 'r') as archivo:

	    # Crea un lector de CSV
	    lector_csv = csv.reader(archivo)

	    closes = []
	    fechaApertura = []
	    # Lee la primera fila y guarda el primer valor de cada línea
	    
	    closes = [linea[0] for linea in lector_csv if len(linea) > 0]
	    archivo.seek(0)
	    fechaApertura = [linea[1] for linea in lector_csv if len(linea) > 1]

	    closes = numpy.array(closes, dtype= numpy.float64)
	    try:
	    	_, _, histograma = talib.MACD(closes, fastperiod=i, slowperiod=j, signalperiod=k)

	    except:
	    	print("error con: ",i,j,k)
	    	histograma = []

	    return closes, fechaApertura, histograma



#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

if __name__ == '__main__':

	date_format = '%Y-%m-%d %H:%M:%S'
	profitR = 0.00
	profitRdeR = 0.00
	operacionesTotal = 0
	perdidas = 100
	intervalo = '3m'
	rango= range(2,31)
	fast = 0
	slow = 0
	signal = 0
	#k = 9
	#for numero in range(-50, 1, 10):
	for numero in [-50]:

		for numero2 in [50]:

			# i = 11
			# j = 12
			# k = 27

		#for numero2 in range(50, -1, -10):
		
		#for i,j,k in itertools.product(rango,rango,rango):

			inicio = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
			final = inicio + datetime.timedelta(days=1)

			#path = 'datos_historicos_ETHBUSD/MAYO_2023_'+intervalo+'.csv'
			
			#Iterar sobre los días de noviembre
			while inicio <= datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'):
				finicio = inicio.strftime(date_format)
				ffinal = final.strftime(date_format)

				closes, FechaApertura = calculo_datos(intervalo,finicio,ffinal)
				escribir_csv(closes, FechaApertura, finicio, intervalo)

				posicion = 0.00
				saldoinicial = saldo
				saldo = saldoinicial

			#closes, FechaApertura, histograma_minutely = leer_cal_datos(path,i,j,k)

			# if len(histograma_minutely) > 0:

			# 	numero, numero2, perdidasT, operacionT, profitR = macdprueba(float(-20), float(20), histograma_minutely, closes, FechaApertura)
				
			# 	print("fast: ",i,"slow: ",j,"signal: ",k,"-> profit: ",profitR,"operaciones: ", operacionT,"perdidas: ", perdidasT)
			# 	profitDia = ((saldo-saldoinicial)*100)/saldoinicial
			# 	#print(finicio,"----",ffinal, ": ", profitDia,"\n")

			# 	profits.append(profitDia)
				inicio += datetime.timedelta(days=1)  # Suma un día a la fecha actual
				final += datetime.timedelta(days=1)  # Suma un día a la fecha siguiente
			# 	operacionT += operaciones
			# 	perdidasT += perdidasi
			# profitR = sum(profits)/float(len(profits))
			# print(profitR, numero,numero2)

			#if  perdidasT < perdidas and operacionT > operacionesTotal and profitR > profitRdeR:
			# if perdidasT < perdidas:
			# 	fast = i
			# 	slow = j
			# 	signal = k
				
			# 	profitRdeR = profitR
			# 	intervaloR = intervalo
			# 	saldo1 = saldo
			# 	entrada = numero
			# 	salida = numero2
			# 	operacionesTotal = operacionT
			# 	perdidas = perdidasT
			# 	encontrado = True


	#*************************************************************************************
	#print("Con:", TipoOperacion)
	if encontrado:

		print("*******************************************")
		#print("con hist")
		print("con macd")
		print("El que mejor resultado tuvo fue")
		print(f"fast: {fast}, slow: {slow}, signal; {signal}")
		print(f"Long entrada: {entrada}, salida: {salida} \nShort entrada: {salida}, salida: {entrada}")
		print(f" en {operacionesTotal} operaciones")
		print(f" en intervalos de {intervaloR}")
		total = ganancias + (perdidas*-1)
		if total == 0.00:
			total = 1
		print("perdidas totales: ", perdidas)
		print(f"***************\n {saldoinicial1}$ se transformaron en {saldo1:.2f}$")
		print(f"profit: {profitRdeR:.2f}%")
	else: 
		print("no se encontro un profit bueno")
	print()


#rainer probar estrategia 21 14 8, y tambien ver como se puede usar el impulse macd
