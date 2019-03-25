#Create 2 automated tests that verify the Create and Remove user functionality under /Manage/Users (UI test automation)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import pandas as pd
from bs4 import BeautifulSoup
import pdb

#Read Input Files
login_info_filename = 'logininfo.csv'
user_info_filename = 'userinfo.csv'
test_report_filename = 'test_report.csv'

class create_user:
	def create_user_driver(self,usr):
		#Read Driver Info
		driver = webdriver.Chrome(executable_path=r'C:\Users\Vijay.Parkale\Desktop\Vijay_Data\chromedriver_win32\chromedriver.exe')
		driver.get("https://wpm-trial.apicasystem.com/Users")
		assert "Apica Synthetic Portal" in driver.title

		login_info_df = pd.read_csv(login_info_filename)
		user_info_df = pd.read_csv(user_info_filename)
		#Read Username and Passwordbto Login
		username = login_info_df.iloc[0]['username']
		password = login_info_df.iloc[0]['password']

		elem = driver.find_element_by_id("username")
		elem.send_keys(username)
		elem = driver.find_element_by_id("password")
		elem.send_keys(password)

		elem.send_keys(Keys.RETURN)
		driver.find_element_by_id("first_time_new_user").click()
		line_number1 =user_info_df[user_info_df['username1']==usr].index.tolist()[0]
		#Read User Info from .csv file to create new user
		
		username1 = user_info_df.iloc[line_number1]['username1']
		fullname = user_info_df.iloc[line_number1]['fullname']
		phone = str(user_info_df.iloc[line_number1]['phone'])
		mobile = str(user_info_df.iloc[line_number1]['mobile'])
		new_password = user_info_df.iloc[line_number1]['new_password']
		confirmed_password = user_info_df.iloc[line_number1]['confirmed_password']
		#Create User using above Information
		elem1 = driver.find_element_by_id("username")
		elem1.send_keys(username1)
		elem1 = driver.find_element_by_id("fullname")
		elem1.send_keys(fullname)
		elem1 = driver.find_element_by_id("phone")
		elem1.send_keys(phone)
		elem1 = driver.find_element_by_id("mobile")
		elem1.send_keys(mobile)
		elem1 = driver.find_element_by_id("password")
		elem1.send_keys(new_password)
		elem1 = driver.find_element_by_id("password-2")
		elem1.send_keys(confirmed_password)
		
		#call click button()
		driver.find_element_by_id("create-user-btn").click()

	def  check_create_user(self,usr):
		#Read Driver Info
		driver = webdriver.Chrome(executable_path=r'C:\Users\Vijay.Parkale\Desktop\Vijay_Data\chromedriver_win32\chromedriver.exe')
		driver.get("https://wpm-trial.apicasystem.com/Users")
		assert "Apica Synthetic Portal" in driver.title

		login_info_df = pd.read_csv(login_info_filename)
		user_info_df = pd.read_csv(user_info_filename)
		test_info_df = pd.read_csv(test_report_filename)
		
		#Read Username and Passwordbto Login
		username = login_info_df.iloc[0]['username']
		password = login_info_df.iloc[0]['password']

		elem = driver.find_element_by_id("username")
		elem.send_keys(username)
		elem = driver.find_element_by_id("password")
		elem.send_keys(password)

		elem.send_keys(Keys.RETURN)
		
		soup_level1=BeautifulSoup(driver.page_source, 'lxml')
		My_table = soup_level1.find('table',{'class':'usertable'})
			 
		rows = My_table.findAll('tr')
		usr_names = []
		for row in rows:
			try:
				val = row.findAll('td')[0].text
				if len(val)>0:
					usr_names.append(val)
			except:
				pass
		if usr in usr_names:
			test_info_df = test_info_df.append({'id_usrname':usr, 'testcase':'create new user','result':'PASS'}, ignore_index=True)
			test_info_df.to_csv(test_report_filename,index=False)
		else:
			test_info_df = test_info_df.append({'id_usrname':usr, 'testcase':'create new user','result':'FAIL'}, ignore_index=True)
			test_info_df.to_csv(test_report_filename,index=False)

cr_user_obj = create_user()
cr_user_obj.create_user_driver('rony@abc.com')
cr_user_obj.check_create_user('rony@abc.com')
#cr_user_obj.check_create_user('rahul@abc.com')






