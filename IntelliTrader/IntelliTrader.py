
from kiteconnect import KiteConnect
from connection import Connection
import os
import pandas as pd

user_cred_path = "./assets/user_credentials.txt"
config = open(user_cred_path,'r').read().split()

# Begin connection
c = Connection(config)
kite, request_token, access_token = c.broker_login(KiteConnect)
kite.set_access_token(access_token)

