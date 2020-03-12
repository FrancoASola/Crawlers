## Miami Dade Crawler--Future Auctions

## v1 4/6/2018

## Write CSV Files

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as soup

#Open Chrome website an navigate to website
driver = webdriver.Chrome()
driver.get('https://www.miamidade.realforeclose.com/index.cfm?zaction=AUCTION&zmethod=PREVIEW&AuctionDate=11/06/2018')
numpg=2

maxpg=numpg+1

#Create Files
filenamef= "auctionsforeclose.csv"
ff=open(filenamef,'a')
headers= "Auction Status , Auction Type, Sold To, Sold Amount Case #, Opening Bid, Parcel ID, Property Address, Assessed Value\n"
#ff.write(headers)
filenamet= "auctionstaxdeed.csv"
ft=open(filenamet,'a')
headers= "Auction Status , Auction Type, Case #, Certificate #, Opening Bid, Parcel ID, Property Address, Assessed Value\n"
#ft.write(headers)

#Pull Data
for i in range(1,maxpg):
    
    source = driver.page_source 
    #Click Next
    nextpg=driver.find_element_by_class_name("PageRight").click()
    
    try:
        element=WebDriverWait(driver, 1).until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, "ASTAT_MSGA ASTAT_LBL"),"Auction Status"))
    except TimeoutException:
        print("Timeout Error") 
                 
    page_soup = soup(source, "html.parser")
    Head_W = page_soup.find("div",{"class":"Head_W"})
    auctions = Head_W.findAll("div",{"class":"AUCTION_ITEM PREVIEW"})
    auctions = auctions+Head_W.findAll("div",{"class":"AUCTION_ITEM PREVIEW adc-spacer"})
    
    #Organize Data
    for auction in auctions:

        Auction_Status = auction.findAll("div",{"class":"ASTAT_MSGB Astat_DATA"})
        Status = Auction_Status[0].text
        if Status=="Canceled per County" or Status=="Redeemed" or Status=="Canceled per Order" or Status=="Canceled per Bankruptcy":
            continue
        
        Auction_Status= auction.findAll("div",{"class":"ASTAT_MSGB Astat_DATA"})
        Status= Auction_Status[0].text
        Auction_Info= auction.findAll("td",{"class":"AD_DTA"})
        Type=Auction_Info[0].text
        Foreclose_Info=auction.findAll("td",{"class":"AD_DTA"})
        
        #Foreclosure Auctions
        if Type=="FORECLOSURE":
            continue
            Sold_Amount=auction.findAll("div",{"class":"ASTAT_MSGD Astat_DATA"})
            Sold_Amount=Sold_Amount[0].text
            Sold_To=auction.findAll("div",{"class":"ASTAT_MSG_SOLDTO_MSG Astat_DATA"})
            Sold_To=Sold_To[0].text
            Case_Number=Auction_Info[1].text.strip()
            Final_Judge=Auction_Info[2].text           
            ParcelID=Auction_Info[3].a.get('href')
            ParcelID_text=Auction_Info[3].text
            if ParcelID_text=="LIQOURLICENSE":
                continue
            
            Address=Auction_Info[4].text
            if ParcelID_text=="LIQOURLICENSE" or ParcelID_text=="TIMESHARE" or ParcelID_text=="Property Appraiser": 
                Location="N/A"
                Assessed_Value="N/A"
            else:
                Location=Auction_Info[5].text
                Assessed_Value=Auction_Info[6].text
        
            ff.write(Status + "," + Type + "," + Sold_To + "," + Sold_Amount.replace(",","  ") + "," + Case_Number + "," + 
                     Final_Judge.replace(",","  ") + "," + ParcelID + "," + Address+ (" ")+ Location.replace(",","|") + "," + 
                     Assessed_Value.replace(",","  ") + "\n")

        #Taxdeed
        else:
            Case_Number=Auction_Info[1].text.strip()
            Certificate=Auction_Info[2].text
            Opening_Bid=Auction_Info[3].text
            ParcelID=Auction_Info[4].a.get('href')
            Address=Auction_Info[5].text
            Location=Auction_Info[6].text
            if Auction_Info[-1]==Auction_Info[6]:
                Assessed_Value="Not Available"
       
            else:
                Assessed_Value=Auction_Info[7].text
    
            ft.write(Status + "," + Type + "," + Case_Number + "," + Certificate + "," + Opening_Bid.replace(",","  ") 
                     + "," + ParcelID + "," + Address+Location.replace(",","|") + "," + Assessed_Value.replace(",","  ") + "\n")

driver.quit()
ff.close()    
ft.close()