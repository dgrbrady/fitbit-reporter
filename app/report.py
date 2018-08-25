import fitbit
from python_fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime

# Fitbit API
CLIENT_ID = '22CYQZ'
CLIENT_SECRET = 'c7e1bcdaa290204bbdb8ec429523f9d0'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()