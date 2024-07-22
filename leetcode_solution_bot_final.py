import json
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LeetCodeScraper:
    BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    WEB_URL = "http://leetcode.ca/all/problems.html"
    START_SOLUTION_NUMBER = 300
    MAX_SOLUTION_NUMBER = 500
    SCROLL_AMOUNT = 100
    LANGUAGE = 'Javascript' #Java,Python,C++,Javascript Note: if it is java first click on python and then on java

    def __init__(self):
        self.code_dict = {}
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.BRAVE_PATH
        self.driver = webdriver.Chrome(options=self.options)

    def get_sum_link(self, link):
        try:
            self.driver.get(link)
            question_title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[@class='div-width']/h1"))).text

            try:
                premium_check = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, ".//span[@class='label label-info' and contains(text(), 'Prime')]"))
                )
                print("Premium element found")
                self.driver.get(self.WEB_URL)
            except TimeoutException:
                pass

            solutions_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '(.//a[contains(@style, "decoration:underline")])[1]'))).get_attribute(
                "href")
            self.driver.get(solutions_link)

            time.sleep(2)

            # If Java is selected then replace LANGUAGE to python in below line
            python_lang = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{LeetCodeScraper.LANGUAGE}' and @aria-expanded='false']")))
            python_lang.click()

            # Enable this when u want to scrape java data or else comment next two lines
            # java_lang = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, f"//a[text()='{LeetCodeScraper.LANGUAGE}' and @aria-expanded='false']")))
            # java_lang.click()

            code_element_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li[@class='uk-active']//code"))).text

            first_class_index = code_element_text.find("class Solution:")
            second_class_index = code_element_text.find("class Solution:", first_class_index + 1)

            if second_class_index != -1:
                extracted_code = code_element_text[:second_class_index]
            else:
                extracted_code = code_element_text

            self.code_dict.update({question_title: extracted_code})
            self.driver.get(self.WEB_URL)
            time.sleep(5)

        except (NoSuchElementException, TimeoutException):
            self.driver.get(self.WEB_URL)
            time.sleep(5)
        except ElementClickInterceptedException:
            python_lang = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{LeetCodeScraper.LANGUAGE}' and @aria-expanded='false']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", python_lang)
            python_lang.click()

    def iterate_links(self):
        scroll_amount = self.SCROLL_AMOUNT
        for i in range(self.START_SOLUTION_NUMBER, self.MAX_SOLUTION_NUMBER):
            try:
                scroll_amount += 30
                sum_link = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f".//a[@href='{i}.html']"))).get_attribute('href')
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(3)
                self.get_sum_link(sum_link)

            except TimeoutException:
                pass

    def scrape(self):
        try:
            self.driver.get(self.WEB_URL)
            self.driver.maximize_window()
            self.iterate_links()

            json_file_name = "code_solutions_javascript_2.json"
            with open(json_file_name, "w") as json_file:
                json.dump(self.code_dict, json_file, indent=4)

            # input("Enter:")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    scraper = LeetCodeScraper()
    scraper.scrape()
