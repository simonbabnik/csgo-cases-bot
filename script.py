from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import selenium
import selenium.webdriver as webdriver
import time

# writing in csv file
filename = "cases.csv"
f = open(filename, "w")
headers = "name, quantity, price (USD)\n"
f.write("sep=,\n")
f.write(headers)

driver = webdriver.Chrome()

for page_num in range(1,4):

    print(page_num)
    #connection
    url = 'https://steamcommunity.com/market/search?q=Case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730#p' + str(page_num) +'_name_asc'

    print(url)
    driver.get(url)

    pagesource = driver.page_source

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    #parsing
    page_soup = soup(pagesource, "html.parser")

    #finds each case
    containers = page_soup.findAll("div", {"class":"market_listing_row"})

    for container in containers:
        # case name
        name = list(container.find("span", {"market_listing_item_name"}))[0].strip()
        print(name)

        # number of cases
        quantity = container.find("span", "market_listing_num_listings_qty")["data-qty"]
        print("Quantity:", quantity)

        # price of one case
        price1 = container.find("span", {"class": "normal_price"})
        price2 = float(price1.span["data-price"]) / 100.0
        print(price2)

        f.write(str(name) + "," + str(quantity) + ", " + str(price2) + "\n")


    driver.find_element_by_xpath("//*[@id='searchResults_btn_next']").click()
    time.sleep(2)

f.close()