# import math

# norm = 0.0
# length = 9
# weight = []


# for i in range(length):

#   weight.append((length-i)*length)
#   norm += (length-i)*length

# print(weight)
# print(len(weight))
# print(norm)
# print(type(round(math.sqrt(9))))
# print(weight[3:])

"""

y = 5
x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
lst = []
norm = 0.0
sum_ = 0.0
for i in range(y):
    weight = (y - i) * y
    print("weight en la iteración ", i, ": ", weight)
    norm = norm + weight
    sum_ = sum_ + x[i] * weight
    _wma = sum_ / norm
    lst.append(_wma)
    
print("Valores de WMA: ", lst)


weight = [81, 72, 63, 54, 45, 36, 27, 18, 9]




//@version=5
strategy("RSI Strategy", overlay=true)
length = input( 14 )
overSold = input( 30 )
overBought = input( 70 )
price = close
vrsi = ta.rsi(price, length)
co = ta.crossover(vrsi, overSold)
cu = ta.crossunder(vrsi, overBought)
if (not na(vrsi))
  if (co)
    strategy.entry("RsiLE", strategy.long, comment="RsiLE")
  if (cu)
    strategy.entry("RsiSE", strategy.short, comment="RsiSE")
//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)


//@version=5
strategy("Momentum Strategy", overlay=true)
length = input(12)
price = close
momentum(seria, length) =>
  mom = seria - seria[length]
  mom
mom0 = momentum(price, length)
mom1 = momentum( mom0, 1)
if (mom0 > 0 and mom1 > 0)
  strategy.entry("MomLE", strategy.long, stop=high+syminfo.mintick, comment="MomLE")
else
  strategy.cancel("MomLE")
if (mom0 < 0 and mom1 < 0)
  strategy.entry("MomSE", strategy.short, stop=low-syminfo.mintick, comment="MomSE")
else
  strategy.cancel("MomSE")
//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)
"""

suma = 0
for i in range(1,5):

  suma += i
  print(suma)
# factor = 28
# ponderacion = []
# for i in range(1,8):
#   print(i)
#   ponderacion.append(i/factor)
#   print(ponderacion[i-1])
# print()
# print(sum(ponderacion))