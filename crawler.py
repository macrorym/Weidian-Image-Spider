import urllib.request
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains

def url_split(url):
    split = url.split('.webp')
    return split[0]
def save_image(url, name):
    urllib.request.urlretrieve(url, name+".jpg")

def urls_save(urls, name):
    purls = urls.split(',')  
    for i in range(len(purls)):
        purl = url_split(purls[i])
        save_image(purl,name+str(i))
        print('Image ' + str(i) +' saved..')
    print('All Images are saved')
    
def get_weidian_mer(urlss):
    purls = urlss.split(',')
    print('Initializing Browser....')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    broswer = webdriver.Chrome(options=chrome_options)
    keys = ActionChains(broswer)
    broswer.implicitly_wait(20)
    for url in purls:
        urls = []
        broswer.get(url)
        print('Getting Images....')
        # Image Load Only when Scroll to content
        broswer.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        name = broswer.title
        price = broswer.find_element_by_class_name('cur-price').text
        item_imgs = broswer.find_elements_by_class_name('item-img')
        other_imgs = broswer.find_elements_by_class_name('d-image')
        for tag in (item_imgs+other_imgs):
            src = tag.get_property('src')
            tag.location_once_scrolled_into_view
            time.sleep(3)
            urls.append(src)
        print('Saving Images......')
        for i in range(len(urls)):
            url = urls[i]
            if url != None and len(url) > 1:
                urls[i] = url_split(urls[i])
                try:
                    urllib.request.urlretrieve(urls[i], name + ' pr' + price + "/"+str(i)+".jpg")
                except:
                    os.mkdir(name + ' pr' + price)
    print(name + 'are saved.....')
    broswer.close()

if __name__ == '__main__':  
    while True:
        url = input('Enter URLs (separate with ,) :  ')
        get_weidian_mer(url)
