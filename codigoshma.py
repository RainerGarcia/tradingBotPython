import backtrader as bt
class MomentumStrategy(bt.Strategy):
    params = (
        ('length', 12),
    )
    
    def __init__(self):
        self.mom0 = bt.indicators.Momentum(self.data.close, period=self.params.length)
        self.mom1 = bt.indicators.Momentum(self.mom0, period=1)
        
    def next(self):
        if self.mom0 > 0 and self.mom1 > 0:
            self.buy(size=1, exectype=bt.Order.Stop, price=self.data.high[0] + self.params.mintick, 
                     comment="MomLE")
        else:
            self.cancel(self.buy)
            
        if self.mom0 < 0 and self.mom1 < 0:
            self.sell(size=1, exectype=bt.Order.Stop, price=self.data.low[0] - self.params.mintick, 
                      comment="MomSE")
        else:
            self.cancel(self.sell)


# strategy("Momentum Strategy", overlay=true)
# length = input(12)
# price = close
# momentum(seria, length) =>
# mom = seria - seria[length]
# mom
# mom0 = momentum(price, length)
# mom1 = momentum( mom0, 1)
# if (mom0 > 0 and mom1 > 0)
# strategy.entry("MomLE", strategy.long, stop=high+syminfo.mintick, comment="MomLE")
# else
# strategy.cancel("MomLE")
# if (mom0 < 0 and mom1 < 0)
# strategy.entry("MomSE", strategy.short, stop=low-syminfo.mintick, comment="MomSE")
# else
# strategy.cancel("MomSE")

# transcribe este codigo a python

"""
def momentumcalculator(close_array,period):
    # Desplaza los datos por el período dado
    momentum = np.diff(close_array, period)
    
    # # Calcula la diferencia entre los datos y los datos desplazados
    # momentum = close_array - close_shifted
    
    # Elimina los primeros valores que no son válidos debido al desplazamiento
    #close_shifted[:period] = np.nan
    
    # # Calcula el último valor del indicador Momentum
    #mom = momentum[-1]
    
    return momentum

i = 0

mom0 = momentumcalculator(close, length)
mom1 = momentumcalculator(mom0, period=1)

mom0 = mom0.tolist()
mom1 = mom1.tolist()
"""

"""
src = input(close, title="Source")
modeSwitch = input("Hma", title="Hull Variation", options=["Hma", "Thma", "Ehma"])
length = input(55, title="Length(180-200 for floating S/R , 55 for swing entry)")
lengthMult = input(1.0, title="Length multiplier (Used to view higher timeframes with straight band)")

useHtf = input(false, title="Show Hull MA from X timeframe? (good for scalping)")
htf = input("240", title="Higher timeframe", type=input.resolution)

switchColor = input(true, "Color Hull according to trend?")
candleCol = input(false,title="Color candles based on Hull's Trend?")
visualSwitch  = input(true, title="Show as a Band?")
thicknesSwitch = input(1, title="Line Thickness")
transpSwitch = input(40, title="Band Transparency",step=5)

//FUNCTIONS
//HMA
HMA(_src, _length) =>  wma(2 * wma(_src, _length / 2) - wma(_src, _length), round(sqrt(_length)))
//EHMA    
EHMA(_src, _length) =>  ema(2 * ema(_src, _length / 2) - ema(_src, _length), round(sqrt(_length)))
//THMA    
THMA(_src, _length) =>  wma(wma(_src,_length / 3) * 3 - wma(_src, _length / 2) - wma(_src, _length), _length)
    
//SWITCH
Mode(modeSwitch, src, len) =>
      modeSwitch == "Hma"  ? HMA(src, len) :
      modeSwitch == "Ehma" ? EHMA(src, len) : 
      modeSwitch == "Thma" ? THMA(src, len/2) : na

//OUT
_hull = Mode(modeSwitch, src, int(length * lengthMult))
HULL = useHtf ? security(syminfo.ticker, htf, _hull) : _hull
MHULL = HULL[0]
SHULL = HULL[2]

//COLOR
hullColor = switchColor ? (HULL > HULL[2] ? #00ff00 : #ff0000) : #ff9800

//PLOT
///< Frame
Fi1 = plot(MHULL, title="MHULL", color=hullColor, linewidth=thicknesSwitch, transp=50)
Fi2 = plot(visualSwitch ? SHULL : na, title="SHULL", color=hullColor, linewidth=thicknesSwitch, transp=50)
alertcondition(crossover(MHULL, SHULL), title="Hull trending up.", message="Hull trending up.")
alertcondition(crossover(SHULL, MHULL), title="Hull trending down.", message="Hull trending down.")
///< Ending Filler
fill(Fi1, Fi2, title="Band Filler", color=hullColor, transp=transpSwitch)
///BARCOLOR
barcolor(color = candleCol ? (switchColor ? hullColor : na) : na)
"""