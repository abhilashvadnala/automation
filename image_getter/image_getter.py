from bs4 import BeautifulSoup
# from urllib.request import Request,urlopen
# from urllib.parse import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlretrieve
import os 
from pathlib import Path
# from pdf_maker import *
from tqdm import tqdm
from utils import *
import time
import json

def remove_blur(driver,classname="promo"):
    js_script = """var paras = document.getElementsByClassName({});
                   while(paras[0]) {
                   paras[0].parentNode.removeChild(paras[0]);}​""".format(classname)
    driver.execute_script(js_script)


def startup(url,driver,wait):

    try:
        driver.get(url)
        # time.sleep(10)
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='jump_page']")))
        element = driver.find_element_by_xpath("//input[@id='jump_page']")
        pages = driver.find_element_by_xpath("//span[@class='page_of']")
        np = int(pages.text[2:].strip())
        remove_blur(driver,"promo")
        remove_blur(driver,"auto__doc_page_webpack_doc_page_blur_promo orientation_landscape")
        print("pages: ",np)
        # time.sleep(60)
        element.send_keys(Keys.BACK_SPACE)
        for i in tqdm(range(1,np+1),"Loading images"):
            try:

                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(str(i))
                element.send_keys(Keys.RETURN)
                time.sleep(1)
            except ElementNotInteractableException:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(str(i))
                element.send_keys(Keys.RETURN)
                time.sleep(1)
                continue

        html = driver.page_source
        bs = BeautifulSoup(html,"html.parser")
        
    except Exception as e:
        print(f"Error :{e}")
        return
    
    return bs



def make_urls(bs:BeautifulSoup):
    urls=[]
    for img in tqdm(bs.find_all("img",{'class':'absimg'}),"Extracting images: "):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        urls.append(img_url)
    names = [f"image{i:02d}" for i in range(1,len(urls)+1)]
    final_dict = dict(zip(names,urls))
    for k,v in final_dict.items:
        print(f"{k}: {v}\n\n")
    print("\nsaving urls to json.......\n")
    # with open('urls.json','w+') as f:
    #     json.dump(final_dict,f,sort_keys=True,indent=4)
    # print(f"json saved as urls.json in {Path.cwd()}")
   
    return final_dict

def download_images(fd:dict,path = "images_keerthi"):
    p = Path(path)
    if not p.is_dir():
        p.mkdir()
    os.chdir(str(p))

    for key,value in tqdm(fd.items(),"Downloading images "):
        urlretrieve(value,f"{key}.jpg")
    
    os.chdir("..")


if __name__ == "__main__":

    
    url = 'https://www.scribd.com/document/122752267/Keerthi-Keeritalu-Part1'
    driver_path,_,_ = json_parse()
    driver,wait = setup(url,driver_path)
    bs = startup(url,driver,wait)
    urls = make_urls(bs)
    # download_images(urls)
    # make_pdf("images",filename="Keerthi_kireetalu_1")


