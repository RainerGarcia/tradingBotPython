import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from binance.client import Client
import pandas as pd
from simulador_wallet import simulador_wallet
import backtrader as bt
import plotly.graph_objects as go
import plotly.offline as pyo
import math
import talib
from plotly.subplots import make_subplots
# for l in range(5,100):
# #for l in [55]:
#     for lm in range(1,10):
#     #for lm in [1]:

for año in ["2021","2022","2023"]:
    for mes in ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]:

        intervalo='1m'
        operacion_long = False
        operacion_short = False
        operacion = False
        dinero = 15.00
        apalancado = float(1)
        saldoinicial = dinero

        if año == "2023" and mes == "JULIO":

            print("listo")
            break


        wallet = simulador_wallet(dinero, apalancado)
        path = 'datos_historicos_ETHUSDT/'+mes+'_'+año+'_'+intervalo+'.csv'
        closet,FechaAperturat = wallet.leer_cal_datos(path)


        """
        en 24 horas hay:

        1440 de 1 minutos
        480  de 3 minutos
        288  de 5 minutos
        96   de 15 minutos
        """


        # close = closet[:300]
        # FechaApertura = FechaAperturat[:300]

        close = closet
        FechaApertura = FechaAperturat

        #INPUT
        length = 60
        profitDia = 0.00
        profits = []
        negativos = 0.00
        positivos = 0.00
        porcentajeloss = -0.10
        porcentajeWin = 0.10
        stoplossLONG = 1000000.00
        stoplossSHORT = -1000000.00
        stopWinLONG = 1000000.00
        stopWinSHORT = -1000000.00
        liquidacion = 0.00
        listo = False
        HULL = []
        cierres = []
        fechas = []
        hmaultimo = -1
        hmacomparado = -2
        longitudhma = (hmacomparado)*-1
        hullcolor = []
        señales = []
        color = ""
        entrada = True

        # def WMA(precios,n):
        #     #factor = (n*(n+1))/2
        #     factor = 0
        #     wma = []

        #     for i in range(0,len(precios)):            
        #         if i < n:
        #             suma = 0.00
        #             k = i
        #             for j in range(0,i+1):
        #                 factor = n*(n-k)
        #                 suma += (n-j/factor)*precios[j]
        #                 k -= 1
        #             wma.append(suma)   
        #         else:
        #             k = n
        #             suma = 0.00
        #             for j in range(i-(n-1),i+1):
        #                 suma += (k/factor)*precios[j]
        #                 k -= 1
        #             wma.append(suma)
        #     return np.array(wma)

        # def HMA(src,length):
        #     wma1 = WMA(src,round(length/2))
        #     wma2 = WMA(src,length)
        #     wma3 = (2*wma1)-wma2
        #     wma4 = WMA(wma3,round(math.sqrt(length)))
            
        #     return wma4[-1]

        def WMA(src,length):
            weight_sum = sum([ i for i in range(length)])
            wma_sum = sum([src[i]*(i/length) for i in range(length)])
            return wma_sum / weight_sum

        def HMA(src,length):
            indice = round(length/2)
            wma1 = WMA(src[-indice:],round(length/2))
            wma2 = WMA(src,length)
            wma3 = (2*wma1)-wma2
            n = round(math.sqrt(length))
            weight_sum = 1
            wma_sum = wma3*n
            wma4 = wma_sum / weight_sum
            
            return wma4

        for j in range(length-1,len(close)):

            cierres.append(close[j])
            fechas.append(FechaApertura[j])
            closes = []

            for h in range((j+1)-length,j+1):

                closes.append(close[h])

            closes = np.array(closes)
            HULL.append(HMA(closes,length))

            if len(HULL) >= longitudhma:

                if HULL[hmaultimo] > HULL[hmacomparado]:
                    hullcolor = "verde"
                else:
                    hullcolor = "rojo"

                # if not entrada:
                #     color = hullcolor[0]

                # if hullcolor[-1] != color:

                #     color = "listo"
                #     entrada = True

                if entrada:

                    if wallet.saldo <= 10.00:
                        print("se perdio todo el dinero")
                        print(wallet.saldo)
                        break

                    #--------------------------------------------LONG-------------------------------------------------------------------------------------------
                    if hullcolor == "rojo" and not operacion_long and not operacion:
                        print(wallet.saldo)
                        wallet.abrir_operacion(close[j])
                        señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='green',showarrow=True))
                        operacion_long = True
                        operacion = True
                        saldoEntrada = wallet.saldo
                        precio_inicial = float(close[j])
                        fecha_entrada = FechaApertura[j]
                        stoplossLONG = ((precio_inicial*porcentajeloss)/100.00)+precio_inicial
                        stopWinLONG = ((precio_inicial*porcentajeWin)/100.00)+precio_inicial

                        liquidacion = (((saldoEntrada*apalancado)-saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)
                        
                    
                    if operacion_long and operacion:
                        if close[j] <= liquidacion:
                            print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                        #if  hullcolor == "rojo":
                        #if close[j] >= stopWinLONG or close[j] <= stoplossLONG:
                        if close[j] >= stopWinLONG or hullcolor == "verde":
                        #if close[j] >= stopWinLONG:
                            wallet.cerrar_operacion_long(close[j])
                            #señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='cyan',showarrow=True))
                            print(wallet.saldo)
                            operacion_long = False
                            operacion = False
                            print(f"LONG, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[j]}, diferencia {(((close[j]-precio_inicial)/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[j]}")
                            print()
                            profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                            profits.append(profitDia)
                            stoplossLONG = 1000000.00
                            stopWinLONG = 1000000.00
                            saldoinicial = wallet.saldo
                            if (wallet.saldo-saldoEntrada) < 0:
                                negativos += profitDia
                            else:
                                positivos += profitDia

                     #--------------------------------------------SHORT-------------------------------------------------------------------------------------------
                    if hullcolor == "verde" and not operacion_short and not operacion:

                        print(wallet.saldo)
                        wallet.abrir_operacion(close[j])
                        señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='red',showarrow=True))
                        precioapertura = close[j]
                        operacion_short = True
                        operacion = True
                        saldoEntrada = wallet.saldo
                        precio_inicial = float(close[j])
                        fecha_entrada = FechaApertura[j]
                        stoplossSHORT = -(((precio_inicial*porcentajeloss)/100.00)-precio_inicial)
                        stopWinSHORT = -(((precio_inicial*porcentajeWin)/100.00)-precio_inicial)
                        liquidacion = (((saldoEntrada*apalancado)+saldoEntrada)*wallet.posicion*precio_inicial)/((saldoEntrada*apalancado)*wallet.posicion)

                    if  operacion_short and operacion:
                        if close[j] >= liquidacion:
                            print("liquidacion: ",liquidacion,"en precio: ",precio_inicial)

                        #if  hullcolor == "verde":
                        #if close[j] <= stopWinSHORT or close[j] >= stoplossSHORT:
                        if close[j] <= stopWinSHORT or hullcolor == "rojo":
                        #if close[j] <= stopWinSHORT:
                            wallet.cerrar_operacion_short(precioapertura, close[j])
                            #señales.append(dict(x=FechaApertura[j],y=close[j],ax=1,ay=-40,arrowcolor='blue',showarrow=True))
                            print(wallet.saldo)
                            operacion_short = False
                            operacion = False
                            print(f"SHORT, resultado: {wallet.saldo-saldoEntrada}, {precio_inicial} - {close[j]}, diferencia {(((precio_inicial-close[j])/precio_inicial)*100):.2f}%, Fecha: {fecha_entrada} || {FechaApertura[j]}")
                            print()
                            profitDia = ((wallet.saldo-saldoinicial)*100)/saldoinicial
                            profits.append(profitDia)
                            stoplossSHORT = -1000000.00
                            stopWinSHORT = -1000000.00
                            saldoinicial = wallet.saldo
                            if (wallet.saldo-saldoEntrada) < 0:
                                negativos += profitDia
                            else:
                                positivos += profitDia
        try:

            profitfinal = sum(profits)/float(len(profits))
        except:
            profitfinal = 0.00
        print(intervalo, length)
        print(path)
        print(wallet.saldoinicial,"|--|",wallet.saldo)
        print("positivos: ", positivos ,"\negativos: ", negativos)
        print(f"profit: {profitfinal:.2f}%")
        print("##################################################\n")
        print()

        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        # trazo_precios_cierre = go.Scatter(x=fechas,y=cierres,mode='lines',name=intervalo+", "+año+", "+mes)
        # trace = go.Scatter(x=fechas,y=cierres)
        # data = [trace]
        # trazo_wma = go.Scatter(x=fechas,y=HULL,mode='lines',name='WMA, '+str(length),line=dict(color='red'))
        # fig.add_trace(trazo_precios_cierre, secondary_y = False)
        # fig.add_trace(trazo_wma, secondary_y= True)
        # # layout = go.Layout(annotations=señales)
        # # fig = go.Figure(data=data,layout=layout)
        # pyo.plot(fig, filename='preciocierre.html')
        input("perate morrito")


"""
rainer configura bien el servidor vps de amazon, el aws para que puedar entrar en el y usarlo como una pc virtual
ya ethusdt funciona perfectamente con intervalos de 5min y con x20 en apalancamiento excelente !!! gracias a Dios XD
falta codificar el hmaprueba4 en tiempo real, el código de calculo de hull en tiempo real, falta hacer ese
falta tambien ver como interactuar con el testnet, ver como abrir operacion y como cerrar operacion en cierto momento, con el código en tiempo real mas el 
    testnet configurado y viendo como opera en tiempo real en el binance, si eso sale super bien entonces podremos usar el futuros de nuestra cuenta
    con dinero real.

(opcional) ver como obtener los datos via websocket de binance

importante: estudiar y ver como implementar en python wma para calcularlo y que de bien en el calculo hma y así ver si funciona bien dentro del backtesting 
simulado
"""