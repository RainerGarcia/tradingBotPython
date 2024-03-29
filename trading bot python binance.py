from binance.client import Client
import pandas as pd
from os import system
import time
import talib
import threading
import keyboard
import colorama
from colorama import Fore
#Variables
symbol = "BTCUSDT"

#-----------------------------Binance Testnet-----------------------------------
API_KEY = ""
API_SECRET = ""
precio= 0.00
histogram_last = 0.00
PAUSE = True
cerrar = True
HULL = None
length = 55
lengthMult = 1
hullColor = "listo"

saldo = 100000.00000
saldoinicial = saldo
apalancamiento = 1
comision = 0.0004
posicion = 0.00000000
perdidas = 0.00000
ganancias = 0.00000
#saldoAnterior = saldo
#macd_last = None
#signal_last = None
#K = None
#D = None


#precondiciones
client = Client(API_KEY,API_SECRET,tld="com", testnet=True)
interval = Client.KLINE_INTERVAL_1MINUTE

#-------------------FUNCIONES------------------------------------------------------

def cal_macd(client, symbol, interval):

    global histogram_last
    global cerrar
    while cerrar:
        # Obtener los datos de precios del par BTC-USDT en intervalo de tiempo de 1 día
        klines = client.futures_klines(symbol=symbol, interval=interval)

        # Convert to DataFrame
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.set_index('timestamp')

        _, _, histogram = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

        histogram_last = float(histogram[-1])

def precio_actual(client, symbol):
    global precio
    global cerrar
    while cerrar:

        future_ticker = client.futures_symbol_ticker(symbol=symbol)

        precio = float(future_ticker['price'])

def pausar():
    global PAUSE
    while PAUSE:
        if keyboard.is_pressed('p'):
            PAUSE = False
    
def abrir_operacion():

    global precio
    global apalancamiento
    global comision
    global posicion

    posicion = (apalancamiento*saldo)/precio
    posicion -= posicion*comision

def cerrar_operacion_long():

    global precio
    global saldo
    global apalancamiento
    global comision
    global posicion
    

    posicion *= precio
    posicion -= posicion*comision
    saldo = posicion - ((apalancamiento*saldo) - saldo)

def cerrar_operacion_short(precioapertura,resultado):

    global saldo
    global apalancamiento
    global comision
    global posicion
        
    price = precioapertura + resultado
    posicion *= price
    posicion -= posicion*comision
    saldo = posicion - ((apalancamiento*saldo) - saldo)

def weighted_moving_average(data, window):
    weights = np.arange(1, window + 1)
    wma = np.convolve(data, weights[::-1], 'valid') / weights.sum()
    return wma

def hull_moving_average(data: list[float], length: int) -> list[float]:
    half_length = int(length/2)
    
    # Calcula las medias móviles ponderadas:
    first_wma = weighted_moving_average(data,length)
    second_wma = 2*weighted_moving_average(weighted_moving_average(data,half_length),half_length)[:len(first_wma)]

    diff_wmas=second_wma-first_wma
   
    #Calcula raiz cuadrado del periodo 
    sqrtLength=int(np.sqrt(length))
    
    # Ahora calculamos el HMA aplicando una WMA al resultado anterior.
    hull_ma=weighted_moving_average(diff_wmas,sqrtLength)

    return hull_ma[:-(sqrtLength-1)]

def color_hull(HULL, length, lengthMult):

    global precio
    global hullColor
    global cerrar

    while cerrar:
        HULL = hull_moving_average(precio, int(length * lengthMult))
        #hullColor = np.where(HULL > HULL[-2], "verde", "rojo")
        if HULL > HULL[-2]:
            hullColor = "verde"
        else: 
            hullColor = "rojo"




#----------------------------------------------------------------------------------

if __name__ == "__main__":

    colorama.init()
    hilo = threading.Thread(target=pausar)
    hilo.start()

    hilo1 = threading.Thread(target=cal_macd, args=(client, symbol, interval))
    hilo2 = threading.Thread(target=precio_actual, args=(client, symbol))
    hilo3 = threading.Thread(target=color_hull, args=(HULL, length, lengthMult))
    
    hilo1.start()
    hilo2.start()
    hilo3.start()

    while True:
        if (hullColor != None and precio != None and precio != 0.00):
            break

    while PAUSE:
        if saldo <= 1:
            PAUSE = False 
        system('cls')
        print(precio," --- ", hullColor)   
    
#-------------------------------LONG-------------------------------------------------------
#         if  histogram_last < 0.00:
#             precioapertura = precio
#             abrir_operacion()
#             saldoinicial = saldo
#             print(f"operacion en "+ Fore.GREEN +"LONG"+ f" :{precioapertura:.2f}"+ Fore.RESET)
#             while True: 
#                 time.sleep(180)  
#                 if histogram_last > 0.00:
#                     cerrar_operacion_long()
#                     if saldo >= saldoinicial:
#                         print("Cerro en: "+Fore.GREEN + f"{precio}, ganancia de: {saldo-saldoinicial:.2f}$" + Fore.RESET)
#                         ganancias += saldo-saldoinicial
#                         break
#                     else: 
#                         print("Cerro en: "+Fore.RED+ f"{precio}, perdida de: {saldoinicial-saldo:.2f}$"+ Fore.RESET)
#                         perdidas += saldoinicial-saldo
#                         break


# #---------------------------SHORT------------------------------------------------------------
#         elif histogram_last > 0.00:
#             precioapertura = precio
#             abrir_operacion()
#             saldoinicial = saldo
#             print(f"operacion en "+ Fore.RED +"SHORT" +  f" :{precioapertura:.2f}" + Fore.RESET)
#             while True:
#                 time.sleep(180)
#                 if histogram_last < 0.00:
#                     resultado = precioapertura - precio
#                     cerrar_operacion_short(precioapertura,resultado)
#                     if saldo >= saldoinicial:
#                         print("Cerro en: "+Fore.GREEN +f"{precio}, ganancia de: {saldo-saldoinicial:.2f}$"+ Fore.RESET)
#                         ganancias += saldo-saldoinicial
#                         break
#                     else: 
#                         print("Cerro en: "+Fore.RED+f"{precio}, perdida de: {saldoinicial-saldo:.2f}$"+ Fore.RESET)
#                         perdidas += saldoinicial-saldo
#                         break
#         time.sleep(180)


    print("salio del ciclo")
    cerrar = False
    hilo.join()
    hilo1.join()
    hilo2.join()
    hilo3.join()

    total = ganancias + perdidas

    print("\n****************************************************")
    print("saldo inicial: ", saldoinicial)
    print("Saldo total al finalizar operaciones: ", saldo)
    print(f"ganancias: {ganancias:.2f} , {(ganancias*100)/total:.2f}%")
    print(f"perdidas: {perdidas:.2f} , {(perdidas*100)/total:.2f}%")
    print(f"profit: {((saldo1-saldoinicial)*100)/saldoinicial:.2f}%")

    exit()


"""
    macd > signal, positivo
    macd < signal, negativo
    """
