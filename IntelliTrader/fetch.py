import pandas as pd
import os
import datetime as dt
from helper import Helper

class Fetch:
    def __init__(self, object):
        self.prop = object
        self.help = Helper(object)
        self.fetch_instruments()

    # Fetch instruments list
    def fetch_instruments(self):
        instruments_dump = self.prop['k_token'].instruments('NSE')
        self.help.write_output_csv('nse_instruments.csv', instruments_dump)





