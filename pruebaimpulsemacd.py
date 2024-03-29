"""
Este código parece ser un script para la plataforma TradingView. Está escrito en Pine Script y 
se utiliza para crear un indicador personalizado llamado “Impulse MACD” por el autor LazyBear. 
El script calcula una versión modificada del indicador de Convergencia/Divergencia de Medias Móviles (MACD) 
utilizando una combinación de cálculos de Media Móvil Simple (SMA), Media Móvil Suavizada (SMMA) y 
Media Móvil Exponencial de Retardo Cero (ZLEMA). El script también incluye opciones para personalizar 
la longitud de las medias móviles y habilitar los colores de las barras. 
"""

import pandas as pd

def calc_smma(src, len):
    smma = src.rolling(window=len, min_periods=len).mean()
    return smma

def calc_zlema(src, length):
    ema1 = src.ewm(span=length, adjust=False).mean()
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    d = ema1 - ema2
    return ema1 + d

def impulse_macd(df, lengthMA=34, lengthSignal=9):
    src = (df['High'] + df['Low'] + df['Close']) / 3
    hi = calc_smma(df['High'], lengthMA)
    lo = calc_smma(df['Low'], lengthMA)
    mi = calc_zlema(src, lengthMA)

    md = pd.Series(index=src.index)
    md[mi > hi] = mi - hi
    md[mi < lo] = mi - lo
    md.fillna(0, inplace=True)

    sb = md.rolling(window=lengthSignal).mean()
    sh = md - sb

    mdc = pd.Series(index=src.index)
    mdc[src > mi] = 'green'
    mdc[src > hi] = 'lime'
    mdc[src < lo] = 'red'
    mdc[(src < mi) & (src >= lo)] = 'orange'

    df['ImpulseMACD'] = md
    df['ImpulseHisto'] = sh
    df['ImpulseMACDCDSignal'] = sb

"""
Este código define tres funciones: calc_smma, calc_zlema e impulse_macd. Las dos primeras funciones calculan 
los valores de SMMA y ZLEMA respectivamente. La función impulse_macd toma como entrada un DataFrame que contiene 
los precios altos, bajos y de cierre de un instrumento financiero y agrega tres nuevas columnas al DataFrame: 
ImpulseMACD, ImpulseHisto e ImpulseMACDCDSignal. Estas columnas contienen los valores del indicador Impulse MACD 
calculados utilizando los parámetros de entrada lengthMA y lengthSignal.

"""

"""
hlc3 es una abreviatura de “High-Low-Close divided by 3” (Alto-Bajo-Cierre dividido por 3). 
Es una forma común de calcular el precio típico de un instrumento financiero en un período determinado. 
Se calcula sumando los precios alto, bajo y de cierre y dividiendo el resultado entre 3. En el código que 
proporcionaste, hlc3 se utiliza como la fuente de datos (src) para los cálculos del indicador Impulse MACD.
"""

"""
Finalmente, se calcula el valor de md, que es una medida de la diferencia entre el precio típico (mi) 
y las medias móviles suavizadas (hi y lo). Si mi es mayor que hi, entonces md es igual a la diferencia 
entre mi y hi. Si mi es menor que lo, entonces md es igual a la diferencia entre mi y lo. En caso contrario, 
si mi está entre hi y lo, entonces md es igual a 0.
"""

"""
CODIGO EN PINE SCRIPT

study("Impulse MACD [LazyBear]", shorttitle="IMACD_LB", overlay=false)
lengthMA = input(34)
lengthSignal = input(9)
calc_smma(src, len) =>
	smma=na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len
	smma

calc_zlema(src, length) =>
	ema1=ema(src, length)
	ema2=ema(ema1, length)
	d=ema1-ema2
	ema1+d

src=hlc3
hi=calc_smma(high, lengthMA)
lo=calc_smma(low, lengthMA)
mi=calc_zlema(src, lengthMA) 

md=(mi>hi)? (mi-hi) : (mi<lo) ? (mi - lo) : 0
sb=sma(md, lengthSignal)
sh=md-sb
mdc=src>mi?src>hi?lime:green:src<lo?red:orange
plot(0, color=gray, linewidth=1, title="MidLine")
plot(md, color=mdc, linewidth=2, title="ImpulseMACD", style=histogram)
plot(sh, color=blue, linewidth=2, title="ImpulseHisto", style=histogram)
plot(sb, color=maroon, linewidth=2, title="ImpulseMACDCDSignal")

ebc=input(false, title="Enable bar colors")
barcolor(ebc?mdc:na)

"""