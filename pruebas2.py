from binance.client import Client
import colorama
from colorama import Fore
import numpy as np
import itertools
#----------------------------Binance futures------------------------------------
#API_KEY = "B4zR8xuEb19jug5vwrDEmjqhmZrAgHcKxJ7ZHxv3E7896Zy48rzfHDuwwfCBKK8z"
#API_SECRET = "wDJwThdEK0V5Y6SQ6ubTlV1RcbRvpzTWOhNBbPEnn4I7Qg6Rv2affNMlNWwJLsNr"

#-----------------------------Binance Testnet-----------------------------------
#API_KEY = "199c420078b950fc6b4e9c42d5083fe5cde27fdf14b52c5a94a2f3a37f153fd2"
#API_SECRET = "d74500f1eafc05175b83cbc9d31ecad4ae1af259982661e8538bc9a5983f610c"

#client = Client(API_KEY, API_SECRET, testnet=True)

#futures_balances = client.futures_account_balance()
#for balance in futures_balances:
#   print(balance['asset'], balance['balance'])

#colorama.init()
"""
numero = 10
numero1 = 20
numero2 = 2
print("operacion en" + Fore.RED + f"Texto en rojo{numero}")
print(Fore.GREEN + f"Texto en verde{numero}")
print(Fore.YELLOW + "Texto en amarillo")
print(Fore.BLUE + "Texto en azul")
print(Fore.MAGENTA + "Texto en magenta")
print(Fore.CYAN + "Texto en cian")

print(20 + (numero*-1))

numero -= numero2/2

print(numero)

print(float(-numero))

print(40-0)

import datetime

start_date = '2021-11-01 00:00:00'
end_date = '2021-11-30 00:00:00'

# Convertir las cadenas de caracteres a objetos datetime
fecha_actual = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
fecha_siguiente = fecha_actual + datetime.timedelta(days=1)

# Iterar sobre los días de noviembre
while fecha_actual < datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'):
    print(f"Día actual: {fecha_actual}")
    print(f"Día siguiente: {fecha_siguiente}")
    fecha_actual += datetime.timedelta(days=1)  # Suma un día a la fecha actual
    fecha_siguiente += datetime.timedelta(days=1)  # Suma un día a la fecha siguiente

# date_format = '%Y-%m-%d %H:%M:%S'
# start = datetime.strptime(start_date, date_format)
# end = datetime.strptime(end_date, date_format)

# difference = end - start
# minutes = difference.total_seconds() / 60

# print(f'Hay {minutes} minutos entre {start_date} y {end_date}.')


"""

# import csv

# lista1 = [1, 2, 3]
# lista2 = ['a', 'b', 'c']

# # Asegurarse de que ambas listas tengan la misma longitud
# assert len(lista1) == len(lista2)

# # Combinar las listas en una sola lista de tuplas
# filas = zip(lista1, lista2)

# # Escribir las filas en un archivo CSV
# with open('archivo.csv', 'w') as f:
#     writer = csv.writer(f)
#     for fila in filas:
#         writer.writerow(fila)

# import csv

# #Abre el archivo CSV
# with open('backtesting_datos_historicos/ABRIL_2021_15m.csv', 'r') as archivo:

    # Crea un lector de CSV
    # lector_csv = csv.reader(archivo)

    # primera_fila = []
    # segunda_fila = []
    # # Lee la primera fila y guarda el primer valor de cada línea
    
    # primera_fila = [linea[0] for linea in lector_csv if len(linea) > 0]
    # archivo.seek(0)
    # segunda_fila = [linea[1] for linea in lector_csv if len(linea) > 1]

# Imprime las listas resultantes
# for i in range(len(primera_fila)):
#     print(primera_fila[i], segunda_fila[i])

# valor = "5"
# valor2 = "esot es un: "+valor+" ok"
# print(valor2)

# import datetime

# def verificar_anio(cadena_fecha):
#     fecha = datetime.datetime.strptime(cadena_fecha, '%Y-%m-%d %H:%M:%S')
    
#     print(fecha.year, fecha.month, type(fecha.year), type(fecha.month))
#     if fecha.year == 2021:
#         return 2021
#     else:
#         return 2022

# def verificar_mes(cadena_fecha):
#     fecha = datetime.datetime.strptime(cadena_fecha, '%Y-%m-%d %H:%M:%S')
#     if fecha.month == 2:
#         return fecha.month


# cadena_fecha = '2022-02-01 00:00:00'

# anio = verificar_anio(cadena_fecha)
# print(anio)  # Imprime: 2021

# mes = verificar_mes(cadena_fecha)
# print(mes)  # Imprime: 01

import itertools

valor = 0
rango = range(1,31)
for i,j,k in itertools.product(rango,rango,rango):
    valor += 1

    print(i, j, k, "-", valor)

