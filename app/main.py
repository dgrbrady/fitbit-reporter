import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import logging
import webbrowser

# Logging config
logging.basicConfig(
    filename = 'report.log',
    level = 'INFO',
    format = '%(asctime)s [%(levelname)s]: %(message)s'
)

# Fitbit API config
CLIENT_ID = '22CYQZ'
CLIENT_SECRET = 'c7e1bcdaa290204bbdb8ec429523f9d0'

# Time formats
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
today = str(datetime.datetime.now().strftime('%Y-%m-%d'))

logging.info('Starting script...')
logging.info('Use Oauth to start authentication')
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)

logging.info('Spinning up web server')
server.browser_authorize()
print(webbrowser._browsers)
logging.info('Acquiring tokens')
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

logging.info('Connecting to fitbit API')
auth2_client = fitbit.Fitbit(
    CLIENT_ID, 
    CLIENT_SECRET, 
    oauth2 = True, 
    access_token = ACCESS_TOKEN,
    refresh_token = REFRESH_TOKEN
)

logging.info('Fetching heart rate data for last day')
heart_rate = auth2_client.intraday_time_series(
    'activities/heart',
    base_date = yesterday,
    detail_level = '1sec'
)
time_list = []
value_list = []
for i in heart_rate['activities-heart-intraday']['dataset']:
    value_list.append(i['value'])
    time_list.append(i['time'])

heart_frame = pd.DataFrame({'Heart Rate': value_list, 'Time': time_list})
with open('reports/heart/intraday%s.csv'%yesterday, 'a') as csv:
    csv.write('')
    csv.close()

heart_frame.to_csv(
    'reports/heart/intraday%s.csv'%yesterday,
    columns = ['Time','Heart Rate'],
    header = True,
    index = False)