
from kiteconnect import KiteConnect
from src.connection import Connection
from src.helper import Helper
from src.fetch import Fetch
from src.orders import Orders
import os
import glob
import datetime
import pandas as pd
import logging
                          
# Create and configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] #%(lineno)s - %(module)s - Message: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')

user_cred_path = "./assets/user_credentials.txt"
config = open(user_cred_path,'r').read().split()

auth_date = datetime.datetime.now().strftime('%d%H');
access_token_file = './src/output/access_token' + '_' + auth_date +  '.txt'

if os.path.isfile(access_token_file):
    # Generate trading session
    access_token = open('./src/output/access_token' + '_' + auth_date +  '.txt','r').read()
    kite = KiteConnect(api_key=config[0])
    kite.set_access_token(access_token)
    logging.info("Connected to Kite")
else:
    # Remove old access token and request token before generating new one
    old_access_token_files = glob.glob('./src/output/access_token*.txt')
    old_request_token_files = glob.glob('./src/output/request_token*.txt')

    for old_access_token_file in old_access_token_files:
        try:
            os.remove(old_access_token_file)
        except: 
            logging.error("Error while deleting file : ", old_access_token_file)
            exit()

    for old_request_token_file in old_request_token_files:
        try:
            os.remove(old_request_token_file)
        except: 
            logging.error("Error while deleting file : ", old_request_token_file)
            exit()

    # Begin a new connection
    connect = Connection(config)
    kite, access_token = connect.broker_login(KiteConnect, logging)
    kite.set_access_token(access_token)
    logging.info("Connected to Kite")

connection_kit = {
    "kite" : kite,
    "authorize" : access_token,
    "log" : logging
}

help = Helper(connection_kit)
fetch = Fetch(connection_kit)
orders = Orders(connection_kit)
