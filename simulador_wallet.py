import csv
import numpy

class simulador_wallet():

	def __init__(self,saldo,apalancamiento):

		self.saldo = saldo
		self.saldoinicial = saldo
		self.apalancamiento = apalancamiento
		self.comision = 0.0004
		self.posicion = 0.00

	def abrir_operacion(self,precio):
		self.posicion = 0.00
		self.posicion = (self.apalancamiento*self.saldo)/precio
		self.posicion -= self.posicion*self.comision
	def cerrar_operacion_long(self,precio):


		self.posicion *= precio
		self.posicion -= self.posicion*self.comision
		self.saldo = self.posicion - ((self.apalancamiento*self.saldo) - self.saldo)

	def cerrar_operacion_short(self,precioapertura,preciofinal):

		price = precioapertura + (precioapertura - preciofinal)
		self.posicion *= price
		self.posicion -= self.posicion*self.comision
		self.saldo = self.posicion - ((self.apalancamiento*self.saldo) - self.saldo)

	def leer_cal_datos(self,path):

		with open(path, 'r') as archivo:

			# Crea un lector de CSV
			lector_csv = csv.reader(archivo)

			closes = []
			fechaApertura = []
			# Lee la primera fila y guarda el primer valor de cada línea
		    
			closes = [linea[0] for linea in lector_csv if len(linea) > 0]
			closes = numpy.array(closes, dtype= numpy.float64)
			archivo.seek(0)
			fechaApertura = [linea[1] for linea in lector_csv if len(linea) > 1]

			return closes, fechaApertura
