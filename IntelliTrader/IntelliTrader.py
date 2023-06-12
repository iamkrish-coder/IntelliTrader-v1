
from time import sleep
from kiteconnect import KiteConnect
from selenium import webdriver
import pandas as pd
import os
import time

cwd = os.getcwd()
os.chdir(cwd)
browser = webdriver.Chrome()


user_cred_path = "./assets/user_credentials.txt"
user_creds = open(user_cred_path,'r').read().split()

apiKey = user_creds[0]
secretKey = user_creds[1]
userId = user_creds[2]
userPass = user_creds[3]
mfa = user_creds[4]

kite = KiteConnect(api_key=apiKey)

url = kite.login_url()
#initial_token = url.split('request_token=')[1]
#request_token = initial_token.split('&')[0]

#data = kite.generate_session(request_token, api_secret=secretKey)
#kite.set_access_token(data['access_token'])

browser.get(url)
time.sleep(3)

instrument_dump = kite.instruments('NSE')
instrument_df = pd.DataFrame(instrument_dump)

if os.path.exists('./output/'):
    instrument_df.to_csv('./output/NSE_Instruments.csv', index=False)
else :
    os.mkdir('./output/') 
    instrument_df.to_csv('./output/NSE_Instruments.csv', index=False) 

