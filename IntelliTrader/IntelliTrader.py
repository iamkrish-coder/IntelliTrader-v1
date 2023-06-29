
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from src.connection import Connection
from src.helper import Helper
from src.fetch import Fetch
from src.orders import Orders
from src.ticker import Ticker
import os
import glob
import datetime
import pandas as pd
import logging
                          
# Create and configure logger
logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s [%(levelname)s] #%(lineno)s - %(module)s - Message: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')

user_cred_path = "./assets/user_credentials.txt"
config = open(user_cred_path,'r').read().split()

auth_date = datetime.datetime.now().strftime('%d%H');
access_token_file = './src/output/access_token' + '_' + auth_date +  '.txt'

if os.path.isfile(access_token_file):
    # Generate trading session
    api_key=config[0]
    access_token = open('./src/output/access_token' + '_' + auth_date +  '.txt','r').read()
    kite = KiteConnect(api_key)
    kite_ticker = KiteTicker(api_key, access_token)
    kite.set_access_token(access_token)
    logging.info("Connected to Kite with Ticker Data")
else:
    # Remove old access token and request token before generating new one
    old_access_token_files = glob.glob('./src/output/access_token*.txt')
    for old_access_token_file in old_access_token_files:
        try:
            os.remove(old_access_token_file)
        except: 
            logging.error("Error while deleting file : ", old_access_token_file)
            exit()

    old_request_token_files = glob.glob('./src/output/request_token*.txt')
    for old_request_token_file in old_request_token_files:
        try:
            os.remove(old_request_token_file)
        except: 
            logging.error("Error while deleting file : ", old_request_token_file)
            exit()

    # Begin a new connection
    connect = Connection(config)
    kite, kite_ticker, access_token = connect.broker_login(KiteConnect, KiteTicker, logging)
    kite.set_access_token(access_token)
    logging.info("Connected to Kite with Ticker Data")

connection_kit = {
    "kite" : kite,
    "kiteticker": kite_ticker,
    "authorize" : access_token,
    "log" : logging
}

help = Helper(connection_kit)
fetch = Fetch(connection_kit)
orders = Orders(connection_kit)
ticker = Ticker(connection_kit)

ticker_exchange = ''
ticker_symbol = ''
ticker_mode = ''
user_settings = []

itoken = fetch.stream_instrument_token_lookup(ticker_exchange, ticker_symbol)
ticker.connect_to_ticker(itoken, ticker_mode, user_settings)
