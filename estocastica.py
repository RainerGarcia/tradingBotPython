import pandas as pd
from PyQt5 import QtCore

class Estocastica(QtCore.QThread):

	def __init__(self,client,symbol,interval):
		QtCore.QThread.__init__(self)
		self.client = client
		self.symbol = symbol
		self.interval = interval
		self.K = None
		self.D = None

	def calculo_klines(self):
		klines = self.client.futures_klines(symbol=self.symbol, interval=self.interval)
		return klines

	def run(self):
		klines = self.calculo_klines()
		data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
		data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
		data.set_index('timestamp', inplace=True)
		data['close'] = data['close'].astype(float)
		data['high'] = data['high'].astype(float)
		data['low'] = data['low'].astype(float)

		low_min  = data['low'].rolling(window=14).min()
		high_max = data['high'].rolling(window=14).max()

		fastk = 100 * (data['close'] - low_min) / (high_max - low_min)
		slowk = fastk.rolling(window=3).mean()
		slowd = slowk.rolling(window=3).mean()
 
		self.K = slowk.iloc[-1]
		self.D = slowd.iloc[-1]