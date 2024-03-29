# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

import os
import time

try:
    import binance  
except ImportError:  
    print('\nInstalling python-binance...\n')
    os.system('pip install python-binance')
    import binance
    
try:
    import pandas  
except ImportError:  
    print('\nInstalling pandas...\n')
    os.system('pip install pandas')
    import pandas
    
try:
    import ta
except ImportError:  
    print('\nInstalling ta...\n')
    os.system('pip install --upgrade ta')
    import ta
    
try:
    import plotly
except ImportError:  
    print('\nInstalling plotly...\n')
    os.system('pip install plotly')
    import plotly
    

from binance.client import Client
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy

import plotly.io as pio
pio.renderers.default='browser'




# Configura la conexión a Binance Futures
api_key = ''
api_secret = ''
client = Client(api_key, api_secret, testnet=False)

# Define el par de trading y el intervalo de tiempo
symbol = 'BTCUSDT'
interval = '5m'

# Define el rango de fechas
# start_date = '2023-01-01 00:00:00'
# end_date = '2023-03-30 00:00:00'
limit = 1500

# Descarga los datos de velas japonesas de Binance Futures
candles = client.futures_klines(symbol=symbol, interval=interval, limit=limit)

# Convierte los datos a un dataframe de pandas
df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# Elimina las columnas que no se necesitan
df = df.drop(['quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], axis=1)

# Convierte los valores de las columnas a números de punto flotante
df = df.astype(float)

# Convierte el timestamp a formato de fecha y hora
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Convierte el close_time a formato de fecha y hora
df['close_time'] = pd.to_datetime(df['close_time'] + 1, unit='ms')

# Guarda los datos en un archivo CSV
filename = 'C:/Users/raine/Desktop/velas_binance_futures_btcusdt.csv'
df.to_csv(filename, index=False)

# Carga los datos del archivo CSV en un dataframe de pandas
df = pd.read_csv('C:/Users/raine/Desktop/velas_binance_futures_btcusdt.csv')

# Convierte la columna de timestamp a formato de fecha y hora
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

# Convierte la columna de close_time a formato de fecha y hora
df['close_time'] = pd.to_datetime(df['close_time'], format='%Y-%m-%d %H:%M:%S')

df['long_entry'] = numpy.nan
df['long_exit'] = numpy.nan
df['short_entry'] = numpy.nan
df['short_exit'] = numpy.nan

init_time = time.time()

# Calcula el RSI
periods = 14
df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=periods).rsi()

# Define the period for the ATR
atr_period = 14

# Calculate the ATR for the specified period
df['atr'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=atr_period, fillna=False).average_true_range()

st_mult = 0.5

# Define los umbrales de compra y venta del RSI
buy_threshold = 30
sell_threshold = 70

# Define la comisión
commission_rate = 0.0004

# Inicializa las variables para el backtesting
in_position = None
entry_price = 0
entry_time = None
exit_price = 0
exit_time = None
profits = []

# # Recorre todo el dataframe
# for i in range(1, len(df)):
#     # Si el RSI cruza el umbral de compra y no estamos en posición, abrimos una posición larga
#     if df.loc[i-1, 'rsi'] < buy_threshold and df.loc[i, 'rsi'] >= buy_threshold and not in_position:
#         entry_price = df.loc[i, 'close']
#         entry_time = df.loc[i, 'close_time']
#         in_position = True
#         df.loc[i, 'long_entry'] = entry_price
#         print(f'{"LONG ENTRY:":<20} {entry_time} {entry_price:.2f}')
#     # Si el RSI cruza el umbral de venta y estamos en posición larga, cerramos la posición larga
#     elif df.loc[i-1, 'rsi'] > sell_threshold and df.loc[i, 'rsi'] <= sell_threshold and in_position:
#         exit_price = df.loc[i, 'close']
#         exit_time = df.loc[i, 'close_time']
#         profit = (exit_price - entry_price) *100* (1 - 2*commission_rate)/entry_price
#         profits.append(profit)
#         in_position = False
#         df.loc[i, 'long_exit'] = exit_price
#         print(f'{"LONG EXIT:":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')
#     # Si el RSI cruza el umbral de venta y no estamos en posición, abrimos una posición corta
#     elif df.loc[i-1, 'rsi'] > sell_threshold and df.loc[i, 'rsi'] <= sell_threshold and not in_position:
#         entry_price = df.loc[i, 'close']
#         entry_time = df.loc[i, 'close_time']
#         in_position = True
#         df.loc[i, 'short_entry'] = entry_price
#         print(f'{"SHORT ENTRY:":<20} {entry_time} {entry_price:.2f}')
#     # Si el RSI cruza el umbral de compra y estamos en posición corta, cerramos la posición corta
#     elif df.loc[i-1, 'rsi'] < buy_threshold and df.loc[i, 'rsi'] >= buy_threshold and in_position:
#         exit_price = df.loc[i, 'close']
#         exit_time = df.loc[i, 'close_time']
#         profit = (entry_price - exit_price) *100* (1 - 2*commission_rate)/entry_price
#         profits.append(profit)
#         in_position = False
#         df.loc[i, 'short_exit'] = exit_price
#         print(f'{"SHORT EXIT:":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')

stop_loss = None

# Recorre todo el dataframe HACER ESTO MAS RAPIDO
for i in range(1, len(df)):
    if in_position == "long" and df.loc[i, 'close'] <= stop_loss:
        exit_price = df.loc[i, 'close']
        exit_time = df.loc[i, 'close_time']
        profit = (exit_price - entry_price) *100* (1 - 2*commission_rate)/entry_price
        profits.append(profit)
        in_position = None
        df.loc[i, 'long_exit'] = exit_price
        print(f'{"LONG EXIT (SL):":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')
        
    elif in_position == "short" and df.loc[i, 'close'] >= stop_loss:
        exit_price = df.loc[i, 'close']
        exit_time = df.loc[i, 'close_time']
        profit = (entry_price - exit_price) *100* (1 - 2*commission_rate)/entry_price
        profits.append(profit)
        in_position = None
        df.loc[i, 'short_exit'] = exit_price
        print(f'{"SHORT EXIT (SL)):":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')
    
    if df.loc[i-1, 'rsi'] < buy_threshold and df.loc[i, 'rsi'] >= buy_threshold: # Si el RSI cruza el umbral de compra 
        if in_position == 'short':
            exit_price = df.loc[i, 'close']
            exit_time = df.loc[i, 'close_time']
            profit = (entry_price - exit_price) *100* (1 - 2*commission_rate)/entry_price
            profits.append(profit)
            in_position = None
            stop_loss = None
            df.loc[i, 'short_exit'] = exit_price
            print(f'{"SHORT EXIT:":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')
        
        if not in_position:
            entry_price = df.loc[i, 'close']
            entry_time = df.loc[i, 'close_time']
            in_position = "long"
            df.loc[i, 'long_entry'] = entry_price
            print(f'{"LONG ENTRY:":<20} {entry_time} {entry_price:.2f}')
            stop_loss = df.loc[i, 'low'] - st_mult*df.loc[i, 'atr']
            
    elif df.loc[i-1, 'rsi'] > sell_threshold and df.loc[i, 'rsi'] <= sell_threshold and in_position: # Si el RSI cruza el umbral de venta
        if in_position == 'long':
            exit_price = df.loc[i, 'close']
            exit_time = df.loc[i, 'close_time']
            profit = (exit_price - entry_price) *100* (1 - 2*commission_rate)/entry_price
            profits.append(profit)
            in_position = None
            stop_loss = None
            df.loc[i, 'long_exit'] = exit_price
            print(f'{"LONG EXIT:":<20} {exit_time} {exit_price:.2f} PROFIT: {profit:.2f}%')
            
        if not in_position:
            entry_price = df.loc[i, 'close']
            entry_time = df.loc[i, 'close_time']
            in_position = "short"
            df.loc[i, 'short_entry'] = entry_price
            print(f'{"SHORT ENTRY:":<20} {entry_time} {entry_price:.2f}')
            stop_loss = df.loc[i, 'high'] + st_mult*df.loc[i, 'atr']
        
# Calcula la ganancia total
total_profit = sum(profits)
print(f'TOTAL PROFIT: {total_profit:.2f} %')
print(f'total time: {round(time.time() - init_time, 2)}s')


# # Creamos un nuevo dataframe para almacenar las posiciones largas y cortas
# position_df = pd.DataFrame(columns=['entry_time', 'entry_price', 'exit_time', 'exit_price', 'type'])

# # Almacenamos las posiciones largas en el nuevo dataframe
# long_entries = df[df['long_entry'].notnull()]
# long_exits = df[df['long_exit'].notnull()]
# for i in range(len(long_entries)):
#     entry_time = long_entries.iloc[i]['timestamp']
#     entry_price = long_entries.iloc[i]['long_entry']
#     exit_time = long_exits.iloc[i]['timestamp']
#     exit_price = long_exits.iloc[i]['long_exit']
#     # position_df = position_df.append({'entry_time': entry_time,
#     #                                   'entry_price': entry_price,
#     #                                   'exit_time': exit_time,
#     #                                   'exit_price': exit_price,
#     #                                   'type': 'long'}, ignore_index=True)
    
#     position_df = pd.concat([position_df, pd.DataFrame([{'entry_time': entry_time,
#                                       'entry_price': entry_price,
#                                       'exit_time': exit_time,
#                                       'exit_price': exit_price,
#                                       'type': 'long'}])], ignore_index=True)

# # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# # Almacenamos las posiciones cortas en el nuevo dataframe
# short_entries = df[df['short_entry'].notnull()]
# short_exits = df[df['short_exit'].notnull()]
# for i in range(len(short_entries)):
#     entry_time = short_entries.iloc[i]['timestamp']
#     entry_price = short_entries.iloc[i]['short_entry']
#     exit_time = short_exits.iloc[i]['timestamp']
#     exit_price = short_exits.iloc[i]['short_exit']
#     # position_df = position_df.append({'entry_time': entry_time,
#     #                                   'entry_price': entry_price,
#     #                                   'exit_time': exit_time,
#     #                                   'exit_price': exit_price,
#     #                                   'type': 'short'}, ignore_index=True)
    
#     position_df = pd.concat([position_df, pd.DataFrame([{'entry_time': entry_time,
#                                       'entry_price': entry_price,
#                                       'exit_time': exit_time,
#                                       'exit_price': exit_price,
#                                       'type': 'short'}])], ignore_index=True)

# # Creamos una figura de Plotly con dos subplots: uno para el precio y otro para las posiciones largas y cortas
# fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

# # Agregamos el precio al primer subplot
# fig.add_trace(go.Candlestick(x=df['timestamp'],
#                               open=df['open'],
#                               high=df['high'],
#                               low=df['low'],
#                               close=df['close']),
#                               row=1, col=1)

# # Agregamos las posiciones largas y cortas al segundo subplot
# for i in range(len(position_df)):
#     entry_time = position_df.iloc[i]['entry_time']
#     entry_price = position_df.iloc[i]['entry_price']
#     exit_time = position_df.iloc[i]['exit_time']
#     exit_price = position_df.iloc[i]['exit_price']
#     color = 'green' if position_df.iloc[i]['type'] == 'long' else 'red'
#     fig.add_trace(go.Scatter(x=[entry_time, exit_time],
#                               y=[entry_price, exit_price],
#                               mode='lines',
#                               line=dict(color=color, width=2)),
#                               row=2, col=1)

# # Configuramos la figura y la mostramos
# fig.update_layout(height=800, title='Backtesting RSI Strategy')
# fig.show()

# Crea un gráfico de velas japonesas con las posiciones largas y cortas
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Candlestick(x=df['timestamp'],
                              open=df['open'],
                              high=df['high'],
                              low=df['low'],
                              close=df['close'],
                              name='Candlestick'))
fig.add_trace(go.Scatter(x=df['timestamp'],
                          y=df['long_entry'],
                          mode='markers',
                          name='Long Entry',
                          marker=dict(symbol="triangle-up", color='green', size=10)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['timestamp'],
                          y=df['long_exit'],
                          mode='markers',
                          name='Long Exit',
                          marker=dict(symbol="triangle-down", color='green', size=10)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['timestamp'],
                          y=df['short_entry'],
                          mode='markers',
                          name='Short Entry',
                          marker=dict(symbol="triangle-down", color='red', size=10)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['timestamp'],
                          y=df['short_exit'],
                          mode='markers',
                          name='Short Exit',
                          marker=dict(symbol="triangle-up", color='red', size=10)),
              row=1, col=1)




# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['high']+st_mult*df['atr'], name='ATR high'))
# fig.update_layout(title='Average True Range (ATR) high', xaxis_title='Time', yaxis_title='ATR High')

# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['low']-st_mult*df['atr'], name='ATR low'))
# fig.update_layout(title='Average True Range (ATR) low', xaxis_title='Time', yaxis_title='ATR Low')


fig.show()


# 30-70
# TOTAL PROFIT: 1.92 %
# total time: 0.07s
