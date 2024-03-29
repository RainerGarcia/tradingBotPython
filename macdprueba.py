def macdprueba (num1,num2, histograma_minutely, closes):
	posicion = False
	otro = False
	otro2 = False

	profitM = 0.00
	entrada = 0.00
	salida = 0.00

	numero = num1
	numero2 = num2

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

	for i in range(33,len(histograma_minutely)):

		#print(histograma_minutely[i], " ", closes[i])

		#************************  LONG *****************************************			
		if float(histograma_minutely[i]) < float(numero) and posicion == False:
			operaciones += 1
			posicion = True
			otro = True
			precio_inicial = closes[i]

		if float(histograma_minutely[i]) > float(numero2) and posicion == True and otro == True:
			precio_cierre = closes[i]
			posicion = False
			otro = False

			if precio_cierre > precio_inicial:
				gananciasi += precio_cierre - precio_inicial
			else:
				perdidasi += precio_inicial - precio_cierre


# ***************************   SHORT *************************************************

# 		if float(histograma_minutely[i]) < float(numero) and posicion == False:
# 			operaciones += 1
# 			posicion = True
# 			otro2 = True
# 			precio_inicial = closes[i]
	
# 		if float(histograma_minutely[i]) > float(numero2) and posicion == True and otro2 == True:
# 				posicion = False
# 				otro2 = False
# 				if precio_cierre < precio_inicial:
# 					ganancias += precio_inicial - precio_cierre
# 				else:
# 					perdidas += precio_cierre - precio_inicial


	if gananciasi != 0.00:
		profit = gananciasi-perdidasi
		profit = (profit/gananciasi)*100
	else:
		profit = 0.00
	profitM = profit
	entrada = numero
	salida = numero2
	ganancias = gananciasi
	perdidas = perdidasi
	operacionT = operaciones

	return profitM, entrada, salida, ganancias, perdidas, operacionT