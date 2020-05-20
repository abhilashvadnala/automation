from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from getpass import getpass


core_folder = Path.joinpath(Path.home(),"Downloads","softs") # change this to the location where your chromedriver.exe is
print(core_folder)
driver_path = Path.joinpath(core_folder,"chromedriver.exe")

"""
After the browser pops up...you need to enter your email and password from command line on prompt
- then you need to solve the captcha
- After you solve and login...the page will automatically open your edit profile... to test session handling after login
- You need chromedriver working....though.. :(
"""


options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=str(driver_path))
driver.get("https://www.coursera.org/?authMode=login")
try:

    email_ele = driver.find_element_by_xpath("//input[@type='email']")
    email_ele.send_keys(input("Email: "))
    pass_ele = driver.find_element_by_xpath("//input[@type='password']")
    pass_ele.send_keys(getpass("Password: "))
    driver.find_element_by_xpath("//span[contains(text(),'Log in')]").click()
except Exception as e:
    print(f"{e}")
try:

    WebDriverWait(driver, 100).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Edit profile')]"))).click()
except:
    print("Could not find the element within timeout") 

