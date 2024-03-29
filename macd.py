import pandas as pd 
from PyQt5 import QtCore

class Macd(QtCore.QThread):
	def __init__(self,client,symbol,interval):
		
		QtCore.QThread.__init__(self)
		self.client = client
		self.symbol = symbol
		self.interval = interval
		self.histogram_last = None

	def calculo_klines(self):
		klines = self.client.futures_klines(symbol=self.symbol, interval=self.interval)
		return klines

	def run(self):
		klines = self.calculo_klines()
		# Convert to DataFrame
		df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades_count', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
		df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

		# Calculate MACD
		exp1 = df['close'].ewm(span=12, adjust=False).mean()
		exp2 = df['close'].ewm(span=26, adjust=False).mean()
		macd = exp1 - exp2
		signal = macd.ewm(span=9, adjust=False).mean()
		histogram = macd - signal

		# Display histogram value
		self.histogram_last = histogram.iloc[-1]