import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import vectorbt as vbt
from binance.client import Client
from datetime import datetime, timedelta

#-----------------------------Binance Testnet-----------------------------------
API_KEY = "199c420078b950fc6b4e9c42d5083fe5cde27fdf14b52c5a94a2f3a37f153fd2"
API_SECRET = "d74500f1eafc05175b83cbc9d31ecad4ae1af259982661e8538bc9a5983f610c"
client = Client(API_KEY, API_SECRET, tld='com', testnet=True)
interval = client.KLINE_INTERVAL_1MINUTE
symbolTicker = 'BTCUSDT'
start_date = '2022-01-01'
end_date = '2022-01-02'
macd_fast = 12
macd_slow = 26
macd_signal = 9

klines = client.futures_historical_klines(symbolTicker, interval,start_date, end_date)

# Convertir los datos a un DataFrame de pandas
cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(klines, columns=cols)
df = df.astype(float)

# Convertir la columna de timestamp a formato datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Seleccionar la columna de cierre
close = df['close']

# Calcular el MACD y el histograma usando vectorbt
macd = close.vbt.macd(fast=macd_fast, slow=macd_slow, signal=macd_signal)

macd_histogram = macd['histogram']

# Crear un gráfico para cada intervalo
for interval_start, interval_end in zip(macd_histogram.index[:-1], macd_histogram.index[1:]):
    # Seleccionar los datos del intervalo
    interval_data = macd_histogram.loc[interval_start:interval_end]
    print(interval_data)
    # Crear el histograma
    #fig, ax = plt.subplots()
    #sns.histplot(interval_data, bins=50, ax=ax)
    #ax.set(title=f'Histograma del MACD para el intervalo {interval_start} - {interval_end}')
    #plt.show()