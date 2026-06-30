import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/js/"
driver = webdriver.Chrome()
driver.get(url)

file_path = r"d:\python\quotes_data.csv"

try:
    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Author", "Text", "Tags"])
        
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "author")))
        
        while True:
            html_page = driver.page_source
            soup = BeautifulSoup(html_page, "lxml")
            content = soup.find_all("div", {"class": "quote"})
            
            for i in content:
                text = i.find("span", {"class": "text"}).text
                name = i.find("small", {"class": "author"}).text
                tags = ", ".join([tag.text for tag in i.find_all("a", {"class": "tag"})])
                
                writer.writerow([name, text, tags])
            
            try:
                button = driver.find_element(By.XPATH, "//li[@class='next']/a")
                button.click()
                time.sleep(1.5)
            except:
                print("\n created csv file")
                break

except Exception as e:
    print("ERORR")
    print(e)

finally:
    driver.quit()
