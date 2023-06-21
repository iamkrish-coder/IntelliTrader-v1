from tkinter.tix import COLUMN
import pandas as pd
import os
import datetime as dt
from src.helper import Helper

class Fetch:
    def __init__(self, params):
        self.prop = params

    # Fetch instruments list
    def fetch_instruments(self, exchange=None):
        instruments_dump = self.prop['kite'].instruments(exchange)
        if exchange is not None:
            Helper.write_csv_output('instruments' + '_' + exchange + '.csv', instruments_dump)
            self.prop['log'].info('Instruments fetched for exchange %s', exchange)
        else:
            Helper.write_csv_output('instruments.csv', instruments_dump)
            self.prop['log'].info('Instruments fetched successfully')
        return instruments_dump

    # Lookup instrument token 
    def instrument_lookup(self, exchange, symbol):
        nse_instruments_dump = self.prop['kite'].instruments(exchange)
        instrument_df = pd.DataFrame(nse_instruments_dump)
        try:
            instrument_token = instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
            self.prop['log'].info('Instrument token %d obtained for symbol %s', instrument_token, symbol)
            return instrument_token
        except:
            self.prop['log'].warning('Please verify that the symbol name [%s] is present in the specified exchange.' %(symbol))
            exit()
            
    # Fetch historical data for an exchange and symbol    
    def fetch_ohlc(self, exchange, symbol, interval, duration):
        instrument_token = self.instrument_lookup(exchange, symbol)
        data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), interval))
        Helper.write_csv_output('historical_' + exchange + '_' + symbol +  '.csv', data)
        return data

    # Fetch extended historical data for an exchange and symbol with limits   
    def fetch_ohlc_extended(self, exchange, symbol, period_start, interval):
        match interval:
            case "minute":
                lookback_period_threshold = 60
            case "3minute":
                lookback_period_threshold = 100
            case "5minute":
                lookback_period_threshold = 100
            case "10minute":
                lookback_period_threshold = 100
            case "15minute":
                lookback_period_threshold = 200
            case "30minute":
                lookback_period_threshold = 200
            case "60minute":
                lookback_period_threshold = 400
            case "day":
                lookback_period_threshold = 2000
            case _:
                lookback_period_threshold = 1


        instrument_token = self.instrument_lookup(exchange, symbol)
        start_date = dt.datetime.strptime(period_start, '%d-%m-%Y')
        end_date = dt.date.today()
        data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        while True:
            if start_date.date() >= (dt.date.today() - dt.timedelta(lookback_period_threshold)):
                data = data._append(pd.DataFrame(self.prop['kite'].historical_data(instrument_token, start_date, dt.date.today(), interval)), ignore_index=True)
                break
            else:
                end_date = start_date + dt.timedelta(lookback_period_threshold)
                data = data._append(pd.DataFrame(self.prop['kite'].historical_data(instrument_token, start_date, end_date, interval)), ignore_index=True)
                start_date = end_date
    
        Helper.write_csv_output('historical_' + exchange + '_' + symbol + '_' + str(lookback_period_threshold) + '.csv', data)
        return data

    # Fetch quote
    def fetch_quote(self, exchange, symbol):
        quote = self.prop['kite'].quote(exchange+':'+symbol)
        return quote

    # Fetchltp 
    def fetch_ltp(self, exchange, symbol):
        last_traded_price = self.prop['kite'].ltp(exchange+':'+symbol)
        return last_traded_price

    # Fetch orders 
    def fetch_orders(self):
        orders = self.prop['kite'].orders()
        return orders

    # Fetch positions 
    def fetch_positions(self):
        positions = self.prop['kite'].positions()
        return positions

    # Fetch holdings
    def fetch_holdings(self):
        holdings = self.prop['kite'].holdings()
        return holdings