from PyQt5 import QtCore

class Klines(QtCore.QThread):
	
	def __init__(self,client,symbol,interval):
		QtCore.QThread.__init__(self)
		self.client = client
		self.symbol = symbol
		self.interval = interval
		
		self.klines_valor = None


	def run(self):

			self.klines_valor = self.client.futures_klines(symbol=self.symbol,interval=self.interval)