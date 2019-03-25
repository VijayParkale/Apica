#Remove user functionality under /Manage/Users (UI test automation)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import pandas as pd
from bs4 import BeautifulSoup
import pdb
#Read Driver Info
driver = webdriver.Chrome(executable_path=r'C:\Users\Vijay.Parkale\Desktop\Vijay_Data\chromedriver_win32\chromedriver.exe')
driver.get("https://wpm-trial.apicasystem.com/Users")
assert "Apica Synthetic Portal" in driver.title

#Read Input Files
login_info_filename = 'logininfo.csv'
user_info_filename = 'userinfo.csv'
test_report_filename = 'test_report.csv'

class delete_user:
	def delete_user_driver(self,usr):
		test_info_df = pd.read_csv(test_report_filename)
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
		#****
		soup_level1=BeautifulSoup(driver.page_source, 'lxml')
		My_table = soup_level1.find('table',{'class':'usertable'})
		rows = My_table.findAll('tr')
		row_number =None
		for i in range(len(rows)):
			try:
				val = rows[i].findAll('td')[0].text
				if val == usr:
					row_number = i
			except:
				pass
		if row_number ==None:
			test_info_df = test_info_df.append({'id_usrname':usr, 'testcase':'delete new user','result':'FAIL'}, ignore_index=True)
			test_info_df.to_csv(test_report_filename,index=False)
		else:
			req_xpath = "//*[@id='usertable']/tbody/tr["+str(row_number)+"]/td[9]/a"
			link = driver.find_element_by_xpath(req_xpath).click()
			driver.find_element_by_id("delete-user-btn").click()
			obj = driver.switch_to.alert
			obj.accept()
			
			test_info_df = test_info_df.append({'id_usrname':usr, 'testcase':'delete new user','result':'PASS'}, ignore_index=True)
			test_info_df.to_csv(test_report_filename,index=False)
		
del_user_obj = delete_user()
del_user_obj.delete_user_driver('rony@abc.com')





