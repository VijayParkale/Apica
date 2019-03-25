#Create automated tests against our REST API that verify the API to get the results from a “check” 
#and validate it gets a HTTP 200 and that “check” has the enabled property.


import requests
import json
import pdb
import pandas as pd
import requests

URL = "https://api-wpm-trial.apicasystem.com/v3/Checks/44733?auth_ticket=2DBD70BD-0429-4B92-9E6E-0D1C2482C84D"
test_report_filename = 'test_report.csv'
test_info_df = pd.read_csv(test_report_filename)
response = requests.get(URL,auth=('admin@vijayparkale', 'password'))
data = response.json()

api_msg = 'verify the API to get the results from a check and validate it gets a HTTP 200 and that check has the enabled property'
if ("enabled" in data.keys()) and (response.status_code==200):
	test_info_df = test_info_df.append({'id_usrname':'api', 'testcase':api_msg,'result':'PASS'}, ignore_index=True)
	test_info_df.to_csv(test_report_filename,index=False)
else:
	test_info_df = test_info_df.append({'id_usrname':'api', 'testcase':api_msg,'result':'FAIL'}, ignore_index=True)
	test_info_df.to_csv(test_report_filename,index=False)


