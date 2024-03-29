import talib as l
import pandas as pd
import ta.trend as tr

def calculo_klines(client, symbol, interval):
	klines = client.futures_klines(symbol=symbol, interval=interval)
	return klines

def cal_macd(client, symbol, interval):
	
	# Obtener los datos de precios del par BTC-USDT en intervalo de tiempo de 1 día
	klines = calculo_klines(client, symbol, interval)

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
	histogram_last = histogram.iloc[-1]

	return histogram_last

def cal_Estocastica(client, symbol, interval):

	klines = calculo_klines(client, symbol, interval)
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
 
	K = slowk.iloc[-1]
	D = slowd.iloc[-1]
	return K, D

def precio_actual(client, symbol):

	future_ticker = client.futures_symbol_ticker(symbol=symbol)

	precio = future_ticker['price']

	return precio