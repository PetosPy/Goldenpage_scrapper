from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests


class GoldenPagesScrapper:

	def __init__(self, driver_path, business_type, location):
		self.driver = webdriver.Chrome(executable_path=driver_path)
		self.driver.get("https://www.goldenpages.ie/")
		self.business_type = business_type
		self.location = location
		self.driver.maximize_window()

		time.sleep(5)
		try:
			accept_cookies = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
			if accept_cookies:
				accept_cookies.click()
		except:
			pass

	def crawler(self):
		time.sleep(2)
		business_criteria = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='what']")))
		business_criteria.send_keys(self.bussines_type)
		time.sleep(1)
		loc = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='where']")))
		loc.send_keys(self.location)
		loc.send_keys(Keys.ENTER)
		
		time.sleep(3)
		stores = self.driver.find_element_by_class_name("listing_base_link")
		stores.click()

		email = self.driver.find_element_by_xpath("//a[normalize-space()='info@beautyplus.ie']")
		email.click()
		link = self.driver.current_url 
		print(link)


	def collector(self, url):
		response = requests.get("https://www.goldenpages.ie/new-faces-beauty-clinic-dundalk-A91/")
		job_data = response.text
		soup = BeautifulSoup(job_data, "html.parser")
		company_name = soup.find(name="h1", class_="company_name").text
		# print(company_name)
		company_email = soup.select_one(selector="div[class='main_column col_group'] li:nth-child(2)") 

		print(company_email.text)








