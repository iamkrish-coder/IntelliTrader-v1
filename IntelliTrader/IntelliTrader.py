
from kiteconnect import KiteConnect
from connection import Connection
import os
import pandas as pd

user_cred_path = "./assets/user_credentials.txt"
config = open(user_cred_path,'r').read().split()

# Begin connection
c = Connection(config)
kite = c.broker_login(KiteConnect)

instrument_dump = kite.instruments('NSE')
instrument_df = pd.DataFrame(instrument_dump)

if os.path.exists('./output/'):
    instrument_df.to_csv('./output/NSE_Instruments.csv', index=False)
else :
    os.mkdir('./output/') 
    instrument_df.to_csv('./output/NSE_Instruments.csv', index=False) 

