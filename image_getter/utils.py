from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json



def json_parse(path = "configs.json"):
    driver_path = ''
    search = ''
    location = ''
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
    return driver_path,search,location

def setup(url,driver_path,wait_time=100):

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=str(Path(driver_path)))
    wait = WebDriverWait(driver,wait_time)
    
    return driver,wait