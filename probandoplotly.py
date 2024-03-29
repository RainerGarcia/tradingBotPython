import talib
import plotly.graph_objs as go
import numpy as np
    
def obtener_klines_formateado(simbolo, str_inicio, str_final, vela, dataframe = True, url_base = "https://fapi.binance.com/"):
    
    import datetime
    import traceback
    import requests
    from urllib.parse import urljoin
    import pandas as pd

    def timestamp_ms_to_datetime_str(timestamp_ms):
        return datetime.datetime.fromtimestamp(timestamp_ms/1000).strftime("%Y-%m-%d %H:%M:%S")
    
    timestamp_inicio = datetime.datetime.strptime(str_inicio, "%Y-%m-%d %H:%M:%S").timestamp()
    timestamp_final = datetime.datetime.strptime(str_final, "%Y-%m-%d %H:%M:%S").timestamp()
    
    timestamp_inicio = int(timestamp_inicio*1000) #en ms
    timestamp_final = int(timestamp_final*1000) #en ms
            
    try:
        path = '/fapi/v1/klines'
        
        parametros = {
            'symbol': simbolo,
            'interval': vela,
            'startTime': timestamp_inicio,
            'endTime': timestamp_final,
            'limit': 1500
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



klines = obtener_klines_formateado(simbolo="BTCUSDT", 
                                   str_inicio="2023-05-07 12:00:00", 
                                   str_final="2023-05-07 18:00:00", 
                                   vela = "3m",
                                   dataframe = True)

_, _, histograma = talib.MACD(klines['close'], fastperiod=12, slowperiod=26, signalperiod=9)

fig = go.Figure()
fig.add_trace(go.Scatter(x=klines['open_datetime_str'], y=klines['close']))
colors = np.where(histograma > 0, 'green', 'red')
fig.add_trace(go.Bar(x=klines['open_datetime_str'],y=histograma, marker_color=colors))

fig.show()