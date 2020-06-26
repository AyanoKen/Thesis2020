from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

company = sys.argv[1]

if _ in company:
    company = " ".join(company.split("_"))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get("https://economictimes.indiatimes.com/markets")

driver.implicitly_wait(5)
driver.find_element_by_name("ticker").send_keys(company)
driver.find_element_by_name("ticker").send_keys(Keys.ENTER)

nseTradeprice = driver.find_element_by_id("nseTradeprice").text
nseOpenprice = driver.find_element_by_id("nseOpenprice").text
nseCloseprice = driver.find_element_by_id("nseCloseprice").text
nsetodaychange = driver.find_element_by_id("nseNetchange").text
today_low = driver.find_element_by_css_selector(".dt_lh div:nth-of-type(1) div").text
today_high = driver.find_element_by_css_selector(".dt_lh div:nth-of-type(2) div").text
week52_high_low = driver.find_element_by_css_selector(".d2 ul li:nth-of-type(5) span:nth-of-type(2)").text

respDict = {"Trade Price": nseTradeprice, "Open Price": nseOpenprice, "Close Price": nseCloseprice, "Net Change today": nsetodaychange, "Today's low": today_low, "Today's high": today_high, "52 week low": (week52_high_low).split("/")[0], "52 week high": (week52_high_low).split("/")[1]}

driver.quit()

resp = {
    "Response":200,
    "NSE Data": respDict
}

print(json.dumps(resp))

sys.stdout.flush()
