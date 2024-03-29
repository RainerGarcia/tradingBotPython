from binance.client import Client
from os import system
import threading
import time

#Variables
simbolo = "BTCUSDT"
#----------------------------Binance futures------------------------------------
#API_KEY = "B4zR8xuEb19jug5vwrDEmjqhmZrAgHcKxJ7ZHxv3E7896Zy48rzfHDuwwfCBKK8z"
#API_SECRET = "wDJwThdEK0V5Y6SQ6ubTlV1RcbRvpzTWOhNBbPEnn4I7Qg6Rv2affNMlNWwJLsNr"

#-----------------------------Binance Testnet-----------------------------------
API_KEY = "199c420078b950fc6b4e9c42d5083fe5cde27fdf14b52c5a94a2f3a37f153fd2"
API_SECRET = "d74500f1eafc05175b83cbc9d31ecad4ae1af259982661e8538bc9a5983f610c"
#precondiciones
client = Client(API_KEY,API_SECRET)

class preciosDeBinance():

	def __init__(self,client,simbolo):
		self.client = client
		self.simbolo = simbolo

	#funciones
	def precio_spot(self):
		spot_ticker = self.client.get_symbol_ticker(symbol=self.simbolo)
		return spot_ticker['price']
		
	def precio_futures(self):
		future_ticker = self.client.futures_symbol_ticker(symbol=self.simbolo)
		return future_ticker['price']

	def compra(self,monto,precio):
		total = monto/precio
		time.sleep(10)
		print(f"se compro a {precio}")
		print(f"monto comprado {monto}")
		return total

	def venta(self,monto,precio,apalancamiento):

		total = (monto*precio)
		print(f"se vendio a {spot}")
		print(total)
		total = total - apalancamiento
		print(f"saldo total: {total}")
		print("")
		return total

if __name__ == '__main__':
	"""
	saldo = 10.00
	monto = saldo
	apalancamiento =  (monto*5) - saldo

	while True:
		preciosBinance = preciosDeBinance(client, simbolo)
		spot = 28400#float(preciosBinance.precio_spot())
		future = 28420#float(preciosBinance.precio_futures())
		#system('cls')
		print(f"precio Spot: {spot}, precio futuros: {future}")
		if spot < future:
			monto = monto*5
			monto = preciosBinance.compra(monto,spot)
			time.sleep(5)
			while True:
				spot = 28420#float(preciosBinance.precio_spot())
				future = 28400#float(preciosBinance.precio_futures())
				if spot > future:
					monto = preciosBinance.venta(monto,spot,apalancamiento)					
					break

	"""
	account_info = client.get_account()
	balances = account_info['balances']
	for balance in balances:
		print(balance['asset'], balance['free'])