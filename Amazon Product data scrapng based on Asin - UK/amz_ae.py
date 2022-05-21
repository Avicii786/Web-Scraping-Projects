from glob import escape
from tkinter.tix import CheckList
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os


# drivers path
driver_path = os.getcwd() + '/chromedriver.exe'


# target website url and excel file name
target_url = "https://www.amazon.co.uk/"
input_excel_file = "input_data.xlsx"


# read asin from excel file
df = pd.read_excel(input_excel_file, header=None)
asin_list = df[0]
# asin_list

ser_object = Service(driver_path)
driver = webdriver.Chrome(service=ser_object)
driver.get(target_url)
ex_wait = WebDriverWait(driver, 15)


asin_dict = dict()
product_title_dict = dict()
product_price_dict = dict()
ratings_dict = dict()
other_sellers_data = dict()


for i in range(len(asin_list)):
    try:
        asin_dict[i] = asin_list[i]

        # step 1 : select search box
        search_box = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='twotabsearchtextbox']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys(asin_list[i])

        # step 2 : click Enter to search
        search_box.send_keys(Keys.RETURN)

        # Step 3: capture the price
        try:
            product_price = ex_wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='a-price-whole']")))
            product_price_dict[i] = product_price.text
        except Exception:
            product_price_dict[i] = "NA"

        # step 4 : click on the first product
        product = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")))
        product.click()

        # step 5 : Copy the product title
        product_title = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@id='productTitle']")))
        product_title_dict[i] = product_title.text

        # step 6 : Copy the product ratings
        try:
            product_rating = ex_wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='averageCustomerReviews']//span[@id='acrCustomerReviewText']")))
            ratings_dict[i] = product_rating.text
        except Exception:
            ratings_dict[i] = "No ratings"

        time.sleep(1)
        # step 7: click on the other sellers menu
        # 7: mini step : try this if other seller menu exist
        try:
            other_sellers_menu = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="olpLinkWidget_feature_div"]/div[2]/span/a/div')))
            other_sellers_menu.click()
        # 7 : Except look for the single product details if it is shippe by amazon
        except Exception:
            time.sleep(1)
            check_list = []

            # get the main div
            tabular_buy_box = ex_wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabular_feature_div"]')))
            html1 = tabular_buy_box.get_attribute('innerHTML')
            soup1 = BeautifulSoup(html1, 'html.parser')

            # extract data using bs4
            sh_from = soup1.find_all(
                'span', class_={'a-size-small a-color-tertiary'})[0].text.strip()
            so_by = soup1.find_all(
                'span', class_={'a-size-small a-color-tertiary'})[1].text.strip()
            main_div = soup1.find_all(
                'div', class_={'tabular-buybox-text a-spacing-none'})
            sh_company = main_div[0].text.replace("\n", "").strip()
            so_company = main_div[1].text.replace("\n", "").strip()

            # if loops to check if the data is present or not
            if "amazon" in sh_company.lower() or "amazon.ae" in sh_company.lower() or "amazon.com" in sh_company.lower() or "amazon uk" in sh_company.lower() or "amazon" in so_company.lower() or "amazon.ae" in so_company.lower() or "amazon.com" in so_company.lower() or "amazon uk" in so_company.lower():
                temp_a = f"{sh_from} {sh_company}"
                temp_e_ele_s = f"{so_by} {so_company}"
                check_list.append([temp_a, temp_e_ele_s])
                other_sellers_data[i] = check_list
                print(f"{i} Successfully process : {asin_list[i]}")
            else:
                other_sellers_data[i] = ""
                print(f"{i} Successfully process : {asin_list[i]}")
            continue
        time.sleep(1)
        # Step 8  select see more button  to reveal buy box product details
        seemore_btn = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='aod-pinned-offer-show-more-link']")))
        seemore_btn.click()
        time.sleep(1)
        # Step 9 check buy box prodcut delivery option
        buy_box_check = ex_wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='aod-pinned-offer-additional-content']//div[@id='aod-offer-shipsFrom']//div[@class='a-fixed-left-grid-inner']")))
        # buy_box_check.text
        temp_list = []
        try:
            temp_ele = ex_wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="aod-pinned-offer-additional-content"]/div[1]')))
            html2 = temp_ele.get_attribute('innerHTML')
            soup2 = BeautifulSoup(html2, 'html.parser')
            shipBy2 = soup2.find_all(
                'span', class_={'a-size-small a-color-tertiary'})[0].text.strip()
            soldBy2 = soup2.find_all(
                'span', class_={'a-size-small a-color-tertiary'})[1].text.strip()
            shipBy_company2 = soup2.find(
                'span', class_={'a-size-small a-color-base'}).text.strip()
            test = soup2.find('a', class_={"a-size-small a-link-normal"})
            if test is None:
                soldBy_company2 = soup2.find(
                    'span', class_={'a-size-small a-color-base'}).text.strip()
            else:
                soldBy_company2 = test.get_text().strip()

            if "amazon.ae" in shipBy_company2.lower() or "amazon.com" in shipBy_company2.lower() or "amazon uk" in shipBy_company2.lower() or "amazon" in shipBy_company2.lower() or "amazon.ae" in soldBy_company2.lower() or "amazon.com" in soldBy_company2.lower() or "amazon uk" in soldBy_company2.lower() or "amazon" in soldBy_company2.lower():
                lista = f"{shipBy2} {shipBy_company2}"
                listb = f"{soldBy2} {soldBy_company2}"
                temp_list.append([lista, listb])
        except Exception:
            to_pass = "No data"

        # step 10 : extract those products details which is fullfilled by amazon.ae
        # step 10 Mini step : Select the main div of other sellers
        other_sellers = ex_wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//body/div[@id='all-offers-display']/span[@class='a-declarative']/span[@class='a-declarative']/span[@class='aod-div-for-focus']/div[@id='all-offers-display-scroller']/div[@id='aod-container']/div[@id='aod-offer-list']/div")))
        # look for amazon shipped or sell products
        for j in other_sellers:
            html = j.get_attribute("innerHTML")
            soup = BeautifulSoup(html, parser='html.parser')
            shipFrom = soup.find_all(
                'span', class_='a-size-small a-color-tertiary')[0].text.strip()
            soldBy = soup.find_all(
                'span', class_='a-size-small a-color-tertiary')[1].text.strip()
            shipFrom_company = soup.find_all(
                'span', class_='a-size-small a-color-base')[0].text.strip()
            a = soup.find('a', class_='a-size-small a-link-normal')
            if a is None:
                soldBy_company = soup.find_all(
                    'span', class_='a-size-small a-color-base')[1].text.strip()

            else:
                soldBy_company = a.get_text().strip()
            if "amazon" in shipFrom_company.lower() or "amazon.ae" in shipFrom_company.lower() or "amazon.com" in shipFrom_company.lower() or "amazon uk" in shipFrom_company.lower() or "amazon" in soldBy_company.lower() or "amazon.ae" in soldBy_company.lower() or "amazon.com" in soldBy_company.lower() or "amazon uk" in soldBy_company.lower():
                d_target = f"{shipFrom} {shipFrom_company}"
                sold_by = f"{soldBy} {soldBy_company}"
                temp_list.append([d_target, sold_by])

        other_sellers_data[i] = temp_list

        # step 9 : click on the cross sign to search another asin
        cross_btn = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//i[@aria-label='aod-close']")))
        cross_btn.click()
        print(f"{i} Successfully process : {asin_list[i]}")
    except Exception:
        print("Error in ASIN : ", asin_list[i])
        driver.refresh()

driver.close()
output_data = pd.DataFrame({
    "Asin": asin_dict,
    "Product_Title": product_title_dict,
    "Product_Rating": ratings_dict,
    "Product_Price": product_price_dict,
    "Other_Sellers": other_sellers_data

})


output_data.to_excel("uae_output.xlsx", index=False)
print("Done")
print("All the data stored in uae_output.xlsx")
