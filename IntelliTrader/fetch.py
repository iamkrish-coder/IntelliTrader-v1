import pandas as pd
import os
import datetime as dt
from helper import Helper

class Fetch:
    def __init__(self, object):
        self.prop = object
        self.help = Helper(object)
        self.fetch_instruments_nse()
        self.fetch_instruments_bse()
        #print(self.instrument_lookup('RELIANCE'))
        #self.fetch_ohlc('RELIANCE', '5minute', 5)


    # Fetch instruments list
    def fetch_instruments_nse(self):
        nse_instruments_dump = self.prop['k_token'].instruments('NSE')
        self.help.write_output_csv('nse_instruments.csv', nse_instruments_dump)
        return nse_instruments_dump

    # Fetch instruments list
    def fetch_instruments_bse(self):
        bse_instruments_dump = self.prop['k_token'].instruments('BSE')
        self.help.write_output_csv('bse_instruments.csv', bse_instruments_dump)
        return bse_instruments_dump

    # Lookup instrument token 
    def instrument_lookup(self, symbol):
        nse_instruments_dump = self.prop['k_token'].instruments('NSE')
        instrument_df = pd.DataFrame(nse_instruments_dump)
        try:
            return instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
        except:
            return False

    # Fetch historical data for a symbol    
    def fetch_ohlc(self, symbol, interval, duration):
        instrument = self.instrument_lookup(symbol)
        data = pd.DataFrame(self.prop['k_token'].historical_data(instrument, dt.date.today()-dt.timedelta(duration), dt.date.today(), interval))
        self.help.write_output_csv('historical_' + symbol +  '.csv', data)
        return data