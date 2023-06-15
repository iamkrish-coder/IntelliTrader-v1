
from kiteconnect import KiteConnect
from connection import Connection
from helper import Helper
from fetch import Fetch

import os
import pandas as pd

user_cred_path = "./assets/user_credentials.txt"
config = open(user_cred_path,'r').read().split()

# Begin connection
connect = Connection(config)
kite, request_token, access_token = connect.broker_login(KiteConnect)
kite.set_access_token(access_token)

connection_kit = {
    "k_token" : kite,
    "r_token" : request_token,
    "a_token" : access_token
}

help = Helper(connection_kit)
fetch = Fetch(connection_kit)
