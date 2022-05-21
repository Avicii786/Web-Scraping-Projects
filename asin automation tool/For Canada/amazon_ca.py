# imports
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

target_url = "https://sellercentral.amazon.com/fba/profitabilitycalculator/index?lang=en_CA"  # target url
excel_file_name = "amazon_sheet.xlsx"  # excel file name


# step 1
service_obj = Service(driver_path)
driver = webdriver.Chrome(service=service_obj)
driver.get(target_url)
ex_wait = WebDriverWait(driver, 15)

# reading excel file
data = pd.read_excel(excel_file_name, header=None)
asin_list = data[0]
price_list = data[1]

# step 2 login in to seller central as guest
gues_btn = ex_wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[@aria-labelledby='link_continue-announce']")))
gues_btn.click()


asin_dict = dict()
price_dict = dict()
net_profit_val = dict()
# step 3
for i in range(len(asin_list)):

    try:
        asin_in_box = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='search-string']")))
        # //*[@id="search-string"]
        asin_in_box.clear()
        asin_in_box.send_keys(asin_list[i])
        # step 5
        search_btn = ex_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//input[@type='submit'])[3]")))
        search_btn.click()
        time.sleep(1)
        try:
            pricing_box = ex_wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='afn-pricing']")))
            pricing_box.clear()
            pricing_box.send_keys(price_list[i])
            # step 7
            calculate_btn = ex_wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='update-fees-link-announce']")))
            calculate_btn.click()
            # step 8
            net_profit = ex_wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@id='afn-net-profit']")))
            time.sleep(2)
            print(
                f"{i}: Net Profit for {asin_list[i]} : {net_profit.get_attribute('value')}")
            asin_dict[i] = asin_list[i]
            price_dict[i] = price_list[i]
            net_profit_val[i] = net_profit.get_attribute("value")
            # step 9
            try_another_btn = ex_wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='Try Another Product']")))
            try_another_btn.click()
        except Exception:
            try:
                condition = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div[id='a-popover-2'] div[class='a-popover-wrapper']"))).is_displayed()
                s_btn = ex_wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[value='0']")))
                s_btn.click()
                pricing_box = ex_wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@id='afn-pricing']")))
                pricing_box.clear()
                pricing_box.send_keys(price_list[i])
                # step 7
                calculate_btn = ex_wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@id='update-fees-link-announce']")))
                calculate_btn.click()
                # step 8
                net_profit = ex_wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='afn-net-profit']")))
                time.sleep(2)
                print(
                    f"{i}: Net Profit for {asin_list[i]} : {net_profit.get_attribute('value')}")
                asin_dict[i] = asin_list[i]
                price_dict[i] = price_list[i]
                net_profit_val[i] = net_profit.get_attribute("value")
                # step 9
                try_another_btn = ex_wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@name='Try Another Product']")))
                try_another_btn.click()
            except Exception:
                dim_ele = ex_wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#product-info-dimunit")))
                try_another_pr = ex_wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@name='Try Another Product']")))
                print("Unable to process ASIN : ", asin_list[i])
                asin_dict[i] = asin_list[i]
                price_dict[i] = price_list[i]
                net_profit_val[i] = " "
                try_another_pr.click()
    except Exception:
        print("Unable to process ASIN : ", asin_list[i])
        asin_dict[i] = asin_list[i]
        price_dict[i] = price_list[i]
        net_profit_val[i] = " "
print(f"Total {len(asin_dict)} processed")
driver.close()

outupt_data = pd.DataFrame(
    {"ASIN": asin_dict, "Price": price_dict, "Net Profit": net_profit_val})
outupt_data.to_excel("ca_output.xlsx", index=False)

print("All the data stored in excel file name ca_output.xlsx")
 