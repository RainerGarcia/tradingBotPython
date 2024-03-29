import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from binance.client import Client
import pandas as pd
from simulador_wallet import simulador_wallet
import talib
import backtrader as bt
import plotly.graph_objects as go
import plotly.offline as pyo
import talib
import math
from plotly.subplots import make_subplots
# for l in range(5,100):
# #for l in [55]:
#     for lm in range(1,10):
#     #for lm in [1]:

for año in ["2021","2022","2023"]:
    for mes in ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]:

        intervalo='5m'
        operacion_long = False
        operacion_short = False
        operacion_abierta = False
        dinero = 15.00
        apalancado = float(20)
        saldoinicial = dinero

        if año == "2023" and mes == "JUNIO":

            print("listo")
            break


        wallet = simulador_wallet(dinero, apalancado)
        path = 'datos_historicos_ETHUSDT/'+mes+'_'+año+'_'+intervalo+'.csv'
        close,FechaApertura = wallet.leer_cal_datos(path)


        """
        en 24 horas hay:

        1440 de 1 minutos
        480  de 3 minutos
        288  de 5 minutos
        96   de 15 minutos
        """


        # close = closes[:479]
        # FechaApertura = FechaAperturas[:479]


        #INPUT
        length = 9
        profitDia = 0.00
        profits = []
        negativos = 0.00
        positivos = 0.00
        # porcentajeloss = -0.20
        # porcentajeWin = 1.00
        stoplossLONG = 1000000.00
        stoplossSHORT = -1000000.00
        stopWinLONG = 1000000.00
        stopWinSHORT = -1000000.00
        liquidacion = 0.00
        listo = False

        #FUNCTIONS
        def wma(data, window):

            weights = np.arange(window, 0, -1)
            print(weights)
            weights = weights / weights.sum()
            print(weights)
            return np.convolve(data, weights, mode='same')

        def HMA(src,length):
            #wma1 = wma(src,length/2)
            wma2 = wma(src,length)
            print(wma2)
            print(len(wma2))
            input()
            wma3 = wma((2*wma1)-wma2,round(math.sqrt(length)))
            return wma3

        HULL = HMA(close, int(length))
        hullcolor = []

        for h in range(2,len(HULL)):

            if HULL[h] > HULL[h-2]:

                hullcolor.append("verde")

            else:
                hullcolor.append("rojo")

        close = close.tolist()

        # trace = go.Scatter(x=FechaApertura,y=close)
        # data = [trace]
        # señales = []
        señal = hullcolor[0]

        for j in range(2,len(close)):

            if hullcolor[j-2] != señal:

                señal = "listo"

                if wallet.saldo <= 10.00:
                    print("se perdio todo el dinero")
                    print(wallet.saldo)
                    break

                #--------------------------------------------LONG-------------------------------------------------------------------------------------------
                if hullcolor[j-2] == "verde" and operacion_long == False and operacion_abierta == False:
                    #print(wallet.saldo)
                    wallet.abrir_operacion(close[j])
                    # señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='green',showarrow=True))
                    operacion_long = True
                    operacion_abierta = True
                    saldoEntrada = wallet.saldo
                    precio_inicial = float(close[j])
                    fecha_entrada = FechaApertura[j]
                    # stoplossLONG = ((precio_inicial*porcentajeloss)/100.00)+precio_inicial
                    # stopWinLONG = ((precio_inicial*porcentajeWin)/100.00)+precio_inicial

                    liquidacion = (((saldoEntrada*apalancado)-saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)
                    
                
                if operacion_long == True and operacion_abierta == True:
                    if close[j] <= liquidacion:
                        print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                    #if close[j] >= stopWinLONG or close[j] <= stoplossLONG:
                    if  hullcolor[j-2] == "rojo":
                        wallet.cerrar_operacion_long(close[j])
                        # print(wallet.saldo)
                        operacion_long = False
                        operacion_abierta = False
                        # print(f"LONG, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[j]}, diferencia {(((close[j]-precio_inicial)/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[j]}")
                        # print()
                        profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                        profits.append(profitDia)
                        # stoplossLONG = 1000000.00
                        # stopWinLONG = 1000000.00
                        saldoinicial = wallet.saldo
                        if (wallet.saldo-saldoEntrada) < 0:
                            negativos += profitDia
                        else:
                            positivos += profitDia

                 #--------------------------------------------SHORT-------------------------------------------------------------------------------------------
                if hullcolor[j-2] == "rojo" and operacion_short == False and operacion_abierta == False:

                    # print(wallet.saldo)
                    wallet.abrir_operacion(close[j])
                    # señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='red',showarrow=True))
                    precioapertura = close[j]
                    operacion_short = True
                    operacion_abierta = True
                    saldoEntrada = wallet.saldo
                    precio_inicial = float(close[j])
                    fecha_entrada = FechaApertura[j]
                    #stoplossSHORT = -(((precio_inicial*porcentajeloss)/100.00)-precio_inicial)
                    #stopWinSHORT = -(((precio_inicial*porcentajeWin)/100.00)-precio_inicial)
                    liquidacion = (((saldoEntrada*apalancado)+saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)

                if  operacion_short == True and operacion_abierta == True:
                    if close[j] >= liquidacion:
                        print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                    if  hullcolor[j-2] == "verde":

                        wallet.cerrar_operacion_short(precioapertura, close[j])
                        # print(wallet.saldo)
                        operacion_short = False
                        operacion_abierta = False
                        # print(f"SHORT, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[j]}, diferencia {(((precio_inicial-close[j])/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[j]}")
                        # print()
                        profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                        profits.append(profitDia)
                        #stoplossSHORT = -1000000.00
                        #stopWinSHORT = -1000000.00
                        saldoinicial = wallet.saldo
                        if (wallet.saldo-saldoEntrada) < 0:
                            negativos += profitDia
                        else:
                            positivos += profitDia
        profitfinal = sum(profits)/float(len(profits))
        print(intervalo)
        print(path)
        print(wallet.saldoinicial,"|--|",wallet.saldo)
        print("positivos: ", positivos ,"\negativos: ", negativos)
        print(f"profit: {profitfinal:.2f}%")
        print("##################################################\n")
        print()

        # layout = go.Layout(annotations=señales)
        # fig = go.Figure(data=data,layout=layout)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        trazo_precios_cierre = go.Scatter(x=FechaApertura,y=close,mode='lines',name=intervalo+", "+año+", "+mes)
        trazo_wma = go.Scatter(x=FechaApertura,y=HULL,mode='lines',name='WMA, '+str(length),line=dict(color='red'))
        fig.add_trace(trazo_precios_cierre, secondary_y = False)
        fig.add_trace(trazo_wma, secondary_y= True)
        pyo.plot(fig, filename='preciocierre.html')
        input("gfhdfh")
