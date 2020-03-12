## Broward Crawler

## v1 4/6/2018

## Write CSV Files

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as soup

#CSV File
filenamet= "linksbroward.csv"
ft=open(filenamet,'a')
headers= "Parcel, Map\n"
ft.write(headers)

#Open Chrome website an navigate to website
driver = webdriver.Chrome()
driver.get('')
numpg=5

maxpg=numpg+1


source = driver.page_source 
page_soup=soup(source, "html.parser")
details = page_soup.findAll("tr",{"class":"details selected"})





for i in range(1,maxpg):
    source = driver.page_source 
    page_soup=soup(source, "html.parser")
    details = page_soup.findAll("tr",{"class":"details selected"})
    
    detail=driver.find_elements_by_xpath('//*[@title="Show Details"]')

    for j in range(len(details)):
      
        detail[j].click() 
       
        try:
            element=WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, "label"),"Parcel #:"))
        except TimeoutException:
            print("")

        soupsource= driver.page_source 
    
        psoup= soup(soupsource, "html.parser")
        auctions= psoup.findAll("table",{"class":"bare wrap"})
    for auction in auctions:
        value=auction.findAll("td",{"class":"value"})
        Parcel=value[0].a.get('href')
        Links= value[7].a.get("href")
        ft.write(Parcel + "," + "https://broward.deedauction.net"+Links + "\n")
        print(Parcel)
        print(Links)
    
    j=0
     
       
    nextpg=driver.find_element_by_link_text('Next »')
    nextpg.click()
    
      
    try:
        element=WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, "label"),"Parcel #:"))
    except TimeoutException:
        print("")
    source = driver.page_source 
    page_soup=soup(source, "html.parser")   
    
    
     
 
driver.quit()