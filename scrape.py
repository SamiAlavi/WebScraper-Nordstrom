#! /usr/bin/env python

from time import sleep     # Used for to give time for a page to load from selenium import webdriver
from selenium import webdriver

#read current img (used for resuming program)
with open('img_current.txt','r') as f:
	temp=f.read().split(',')
	
start0,start1,start2,start3,start4 = int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4])
print(f'Resuming from\nTab: {start0}\nCategory: {start1}\nSub-Category: {start2}\nArticle: {start3}\nColor: {start4}')

filter1=[] #enter tab(s) to skip
filter2=[] #enter category/categories to skip
filter3=[] #enter sub-category/sub-categories to skip

driver_path = 'chromedriver.exe'
#options to make selenium faster
prefs = {'profile.default_content_setting_values': {'images': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(driver_path,options=options)

url = 'https://shop.nordstrom.com/'
driver.get(url)
sleep(10)

tabs = driver.find_elements_by_css_selector('button._2PDR1')
tabs = tabs[1:-1]

#tabs
for i in range(start0,len(tabs)):
    tabs = driver.find_elements_by_css_selector('button._2PDR1')
    tabs = tabs[1:-1] #skipping SALE and BRAND tabs
    tab = tabs[i]
    p1 = tab.text
    if p1 in filter1:
        continue
    #print(p1)
    tab.click()
    cats = driver.find_elements_by_css_selector('li > h3.kLGGg > a')
    cats = list(filter(lambda a: a.text != '', cats))
    if i==0 or i==1 or i==2:
        cats = cats[-7:]
    elif i==3:
        cats = cats[-11:]
    elif i==4 or i==6:
        cats = cats[-9:]
    elif i==5:
        cats = cats[-8:]
    links = [cat.get_attribute('href') for cat in cats]
    text1 = [cat.text for cat in cats]
    
    #~categories 1
    for j in range(start1,len(links)):
        p2 = text1[j]
        if p2 in filter2:
            continue
        #print('\t%s'%p2)
        driver.get(links[j])
        cats2 = driver.find_elements_by_css_selector('li._3c707 > a')
        cats2 = list(filter(lambda a: a.text != '', cats2))
        links2 = [cat.get_attribute('href') for cat in cats2]
        text2 = [cat.text for cat in cats2]
        
        #~categories 2
        for k in range(start2,len(links2)):
            links3 = list()
            p3 = text2[k]
            if p3 in filter3:
                continue
            #print('\t\t%s'%p3)
            driver.get(links2[k])
            pages = driver.find_elements_by_css_selector('li._18xGX')
            totalpages = int(pages[-1].text)
            urll = driver.current_url
            
            #go to each page and get link
            for page in range(1,totalpages+1):
                driver.get(f'{urll}&page={page}')
                arts = driver.find_elements_by_css_selector('a._1av3_')
                links3.extend([cat.get_attribute('href') for cat in arts])
                
            lengthlinks = len(links3)
            #~article page
            for l in range(start3,lengthlinks):
                driver.get(links3[l])
                try:
                    title = driver.find_element_by_css_selector('h1._2OMMP').text
                except:
                    title = 'Others'
                try:
                    brand = driver.find_element_by_css_selector('span._1i-_6').text
                except:
                    brand = 'Others'
                colorsbtn = driver.find_elements_by_css_selector('button._3kLmr')
                colorsname = driver.find_elements_by_css_selector('img.zGPcv')
                
                #~every color
                for m in range(start4,len(colorsbtn)):
                    try:
                        closebtn = driver.find_elements_by_id('acsFocusFirst')
                        if len(closebtn)==1:
                            closebtn[0].click()
                        colorsbtn[m].click()
                        p4 = colorsname[m].get_attribute('alt')[9:-6].replace('/','')
                        #print('\t\t\t\t\t%s'%p4)
                        crnt = f"imgs/{p1}/{p2}/{p3}/{brand}/{title}/{p4}"
                        imgs = driver.find_elements_by_css_selector('img._3fwsO')
                        
                        #~write details to files
                        for img in imgs:
                            dwnld = img.get_attribute('src')
                            if dwnld.count('jpeg')==2:
                                dwnld = dwnld[:-10]
                            
                            with open("img_url.txt", "a") as f:
                                f.write(f"{crnt},{dwnld}\n")
                            with open("img_current.txt", "w") as f:
                                f.write(f"{i},{j},{k},{l},{m}")
                    except:
                        with open("img_errors.txt", "a") as f: # write errors
                            f.write(f"{driver.current_url}\n")
                            
                #break
            #break
        #break
    #break    
    driver.get(url)
    sleep(10)

driver.close()

