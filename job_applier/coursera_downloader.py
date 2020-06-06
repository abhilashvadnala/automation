from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from pathlib import Path
from bs4 import BeautifulSoup
import os
import json
import re


driver_path = ''
search      = ''
location    = ''
# match = re.compile('^jl')

def json_parse(path = "configs.json"):
    global driver_path
    global search
    global location
    d = json.load(open (Path.joinpath(Path.cwd(),path),"r",encoding="utf-8"))
    for x in d.values():
        if x.startswith('<'):
            print("ERROR : Please fill in all the values of config file\n")
            exit(0)
    driver_path,search,location= d.values()
         

json_parse()

print(f"driver-path: {driver_path}")
print(f"search-text: {search}")
print(f"search-text: {location}")



"""
After the browser pops up...you need to enter your email and password from command line on prompt
- then you need to solve the captcha
- After you solve and login...the page will automatically open your edit profile... to test session handling after login
- You need chromedriver working....though.. :(
"""
url = 'https://www.glassdoor.com/index.htm'
changed_url = 'https://www.glassdoor.com/member/home/index.htm'

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=str(Path(driver_path)))
driver.get(url)

wait = WebDriverWait(driver,100)
wait.until(EC.url_changes(changed_url))
wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Job Title, Keywords, or Company']")))

try:

    search_ele = driver.find_element_by_xpath("//input[@name = 'sc.keyword']")
    search_ele.send_keys(search)

    location_ele = driver.find_element_by_xpath("//input[@placeholder = 'Location']")
    location_ele.clear()
    location_ele.send_keys(location)

    search_ele.submit()


    source = driver.page_source
    bs = BeautifulSoup(source,'html.parser')
    for x in bs.find_all('a',attrs={'class':'jobInfoItem jobTitle jobLink'}):
        print(x["href"])

except Exception as e:
    print(f"{e}")

# try:

#     email_ele = driver.find_element_by_xpath("//input[@type='email']")
#     email_ele.send_keys(email)
#     pass_ele = driver.find_element_by_xpath("//input[@type='password']")
#     pass_ele.send_keys(password)
#     # email_ele.submit()
#     driver.find_element_by_xpath("//span[contains(text(),'Log in')]").click()
# except Exception as e:
#     print(f"{e}")
# try:

#     WebDriverWait(driver, 100).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
#     WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT, "In Progress"))).click()
# except:
#     print("Could not find the element within timeout") 

