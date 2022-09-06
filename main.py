import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
import os,sys
from bs4 import BeautifulSoup
import pandas as pd

try:
    chromeVersion = os.listdir('C:\Program Files (x86)\Google\Chrome\Application')[0]
except:
    chromeVersion = os.listdir('C:\Program Files\Google\Chrome\Application')[0]
    
chromeVersion = chromeVersion.split('.')
print('Chrome Version :',chromeVersion[0])
currentDirectory = os.getcwd()
options = uc.ChromeOptions()
options.add_argument('--user-data-dir='+currentDirectory+'\\chromeProfile') 
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
driver = uc.Chrome(options=options,use_subprocess=True,version_main=int(chromeVersion[0]))

# Install the VPN extension from the Chrome Store and activate it because the Yell website will not load on the India server.
input('After, Launch the VPN extension and press Enter to proceed.')

# Change the listOfKeywords that you want to search for
listOfKeyword = ['Handicraft','Professional services','Product (business)','Real Estate Agent/Broker','Professional services','Retail Merchandiser','Sports Medicine','Clinical Psychologist','E-Commerce Merchant','E-Commerce Retailer','Apparel Merchandiser','Event Planner','Licensed Real Estate Broker','Manufacturer','E-commerce Strategist','IT and technical services','Legal services','Healthcare and medical services','Cleaning and maintenance services']

for keyword in listOfKeyword:
    print(keyword)
    time.sleep(2)
    driver.get('https://www.yell.com/')
    # URL='https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=858824336&keywords='+keyword+'&location=United+Kingdom'
    # driver.get(URL)
    time.sleep(2)
    
    search = driver.find_element(By.XPATH,'//*[@id="search_keyword"]')
    search.clear()
    search.send_keys(keyword)
    
    location = driver.find_element(By.XPATH,'//*[@id="search_location"]')
    location.clear()
    location.send_keys('United Kingdom')
    time.sleep(2)
    search_button = driver.find_element(By.XPATH,'//*[@id="searchBoxForm"]/fieldset/div[1]/div[3]/button')
    search_button.click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    df = pd.DataFrame()
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        listOfData = soup.findAll('article')
        for data in listOfData:
            website = None
            name = data.find('a',class_='businessCapsule--title').text.strip()
            profile = 'https://www.yell.com'+data.find('a',class_='businessCapsule--title')['href'].strip()
            try:
                phoneNo= data.find('span',class_= 'business--telephoneNumber').text.strip()
            except:
                phoneNo = None
            detailsList = data.findAll('a',class_='btn btn-yellow businessCapsule--ctaItem')
            for detail in detailsList:
                if 'Website' in detail.text:
                    website = detail['href'].strip()
            # print(name)
            # print(profile)
            # print(phoneNo)
            # print(website)
            # print('------------------\n')
            df1 = pd.DataFrame({'Name':[name],
                                'Profile':[profile],
                                'Phone No': [phoneNo],
                                'website':[website]})
            df = pd.concat([df,df1])
        try:
            nextPage = driver.find_element(By.XPATH,'//*[@id="rightNav"]/div[2]/div/div/nav/div[3]/a')
            # print('Next page available')
            nextPage.click()
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except:
            # nextPage = driver.find_element(By.XPATH,'//*[@id="rightNav"]/div[2]/div/div/nav/div[3]/span')
            print('There Is No Next Page')
            print('------------------\n')
            break
    df.to_excel(keyword +'.xlsx',index=False)
driver.close()
driver.quit()