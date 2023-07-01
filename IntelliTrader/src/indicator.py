from asyncio.windows_events import NULL
import os
import datetime as dt
import time
import pandas as pd
from src.helper import Helper
from src.indicators.macd import macd

class Indicator:
    def __init__(self, params):
        self.prop = params

    def execute_handler(self, indicator_option, dataset):
        match indicator_option:
            case 'macd':
                self.option_macd(dataset)
            #case 'rsi':
            #    self.option_rsi(dataset)
            #case 'atr':
            #    self.option_atr(dataset)
            #case 'sma':
            #    self.option_sma(dataset)
            #case 'ema':
            #    self.option_ema(dataset)
            case _:
                self.invalid_option(dataset)

    def option_macd(self, dataset):
        try:
            if dataset is not None and not dataset.empty:
                # Calculate MACD
                pdf = pd.DataFrame(dataset['close'])
                macd_line, signal_line, macd_histogram = macd(pdf)

                # Print the calculated MACD values
                print("\nMACD Line:")
                print(macd_line)

                print("\nSignal Line:")
                print(signal_line)  

                print("\nMACD Histogram:")
                print(macd_histogram)
            else:
                self.prop['log'].error("Failed to calculate MACD") 
                return False
        except:
             self.prop['log'].error("The received object is not a valid DataFrame") 


    def invalid_option(self, dataset):
        # Invalid indicator option provided
        self.prop['log'].warn("The indicator option provided is not valid") 
        