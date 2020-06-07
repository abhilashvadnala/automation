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
import time



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
    print("*********Configs:*************")
    print(f"driver-path: {driver_path}")
    print(f"search-text: {search}")
    print(f"search-text: {location}")
    return

def setup(url):

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=str(Path(driver_path)))
    wait = WebDriverWait(driver,100)
    
    return driver,wait

def login(driver,changed_url,wait):
    """
    Opens the browser and opens the specified url, glassdoor by default.
    Waits for the user to login and the job search text fields to show up.
    """
    try:
            
        driver.get(url)
        wait.until(EC.url_changes(changed_url))
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Job Title, Keywords, or Company']")))
    except Exception as e:
        if "TimeOut" in str(e):
            print("Driver wait timed out\n")
        else:
            print(f"Error:{e}")
    return 

def process_links(links):
    changed_links = []
    for link in links:
        link.replace("GD_JOB_AD","GD_JOB_VIEW")

        if link[0] == '/':
            link = f"https://glassdoor.com{link}"
        
        changed_links.append(link)
    
    # user_agent = 'Mozilla 5.0/'

    return changed_links

def get_urls(driver):


    try:

        search_ele = driver.find_element_by_xpath("//input[@name = 'sc.keyword']")
        search_ele.send_keys(search)

        location_ele = driver.find_element_by_xpath("//input[@placeholder = 'Location']")
        location_ele.clear()
        location_ele.send_keys(location)

        time.sleep(1)

        search_ele.submit()


        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
        )

        time.sleep(5)

        source = driver.page_source
        print("parsing html....")
        bs = BeautifulSoup(source,'html.parser')
        all_anchors = bs.find_all('a',{'class':'jobLink'},href=True)
        print(f"number of anchors extracted: {len(all_anchors)}")
        links = [link['href'] for link in all_anchors]

        print(f"total number of links: {len(links)}")

        changed_links = process_links(links)

        print(f"len of changed links{len(changed_links)}")
        print("************ ALL LINKS *************\n\n")
        print(*changed_links,sep="\n\n\n")


    except Exception as e:
        print(f"{e}")
        return False
    
    return True



if __name__ == "__main__":


    driver_path = ''
    search      = ''
    location    = ''

    url = 'https://www.glassdoor.com/index.htm'
    changed_url = 'https://www.glassdoor.com/member/home/index.htm'

    json_parse()
    driver,wait = setup(url)

    login(driver,changed_url,wait)

    get_urls(driver)



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

