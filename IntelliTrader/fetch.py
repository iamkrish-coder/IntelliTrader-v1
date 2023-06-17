import pandas as pd
import os
import datetime as dt
from helper import Helper

class Fetch:
    def __init__(self, object):
        self.prop = object

    # Fetch instruments list
    def fetch_instruments(self, exchange=None):
        instruments_dump = self.prop['k_token'].instruments(exchange)
        if exchange is not None:
            Helper.write_csv_output('instruments' + '_' + exchange + '.csv', instruments_dump)
        else:
            Helper.write_csv_output('instruments.csv', instruments_dump)
        return instruments_dump

    # Lookup instrument token 
    def instrument_lookup(self, segment, symbol):
        nse_instruments_dump = self.prop['k_token'].instruments(segment)
        instrument_df = pd.DataFrame(nse_instruments_dump)
        try:
            return instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
        except:
            return False

    # Fetch historical data for a segment and symbol    
    def fetch_ohlc(self, segment, symbol, interval, duration):
        instrument = self.instrument_lookup(segment, symbol)
        data = pd.DataFrame(self.prop['k_token'].historical_data(instrument, dt.date.today()-dt.timedelta(duration), dt.date.today(), interval))
        Helper.write_csv_output('historical_' + segment + '_' + symbol +  '.csv', data)
        return data