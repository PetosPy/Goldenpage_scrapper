from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from scrapper_for_goldenpages import GoldenPagesScrapper
import pandas as pd
import openpyxl
from random import randint

###### Search criteria ######
# This is were you enter your criteria
BUSINESS_NAME = "shoe store"
LOCATION = "ireland"


webdriver_path = "C:/development/chromedriver.exe"
headers = {
	"User-Agent": 'https://developers.whatismybrowser.com/useragents/parse/4032336chrome-windows-blink'
}

driver = webdriver.Chrome(executable_path=webdriver_path) 
driver.get("https://www.goldenpages.ie/")

time.sleep(4)
driver.maximize_window()

time.sleep(3)
try:
	accept_cookies = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
	if accept_cookies:
		accept_cookies.click()
except:
	pass

##### Search ######
time.sleep(2)
bussines_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='what']")))
bussines_name.send_keys(BUSINESS_NAME)
time.sleep(1)
location = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='where']")))
location.send_keys(LOCATION)
location.send_keys(Keys.ENTER)

time.sleep(3)
stores = driver.find_elements_by_class_name('listing_title_link')

listofLinks = []
for link in stores:
	links = link.get_property("href")
	listofLinks.append(links)


time.sleep(1)
# products = {}
count = 0

list_of_businesses = []
for i in listofLinks:
	driver.get(i)
	time.sleep(1)
	try:
		name = driver.find_element_by_css_selector("body > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > h1:nth-child(1) > span:nth-child(1)").text
		email = driver.find_element_by_css_selector("div[class='main_column col_group'] li:nth-child(2)").text
	except NoSuchElementException:
		print("No email found")
		pass
	else:
		if email:
			if "@" not in email:
				email = "No email"
		count += 1

		products = {
			"name": name,
			"email": email
		}
		if name in products:
			pass

		list_of_businesses.append(products)
		print(f'item:{count}')

# print(list_of_businesses)
print(len(list_of_businesses))


data = pd.DataFrame(list_of_businesses)
# print(data)


data.to_excel(f"business_data{randint(0,10)}.xlsx")


driver.close()
driver.quit()