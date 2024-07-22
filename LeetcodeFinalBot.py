import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pyperclip
from selenium.webdriver.chrome.options import Options
from code_solutions_python3 import python_json_data
from code_solutions_cplus import cplus_json_data
from code_solutions_java import java_json_data
from code_solutions_javascript import javascript_json_data

class LeetCodeBot:
    LOGIN_URL = "https://leetcode.com/accounts/github/login/"
    PROBLEMSET_URL = "https://leetcode.com/problemset"

    def __init__(self, email, password, language,questions,ui_instance):
        self.email = email
        self.password = password
        self.language = language
        self.questions = int(questions)
        self.driver = None
        self.ui_instance = ui_instance

    def sign_in(self):
        try:
            third_party_page = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,".//button[@type='submit' and text()='Continue']"))
            )
            if not third_party_page.is_displayed():
                print("Third party page not displayed")
                
            else:
                print("Third party page got displayed")
                third_party_page.click()
                # Sign in with credentials
                print("Attempting to find the username input field")
                username_area = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//input[@id='login_field']")))
                username_area.send_keys(self.email)
                
                print("Attempting to find the password input field")
                password_area = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//input[@id='password']")))
                password_area.send_keys(self.password)
                
                print("Attempting to find the sign-in button")
                sign_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//input[@value='Sign in']")))
                sign_button.click()

                # Check for authentication button
                try:
                    print("Waiting for potential authentication button")
                    auth_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//button[@data-octo-click='oauth_application_authorization']")))
                    auth_button.click()
                except TimeoutException:
                    print("Auth button not found, proceeding")
                # Check for Ask me later button
                try:
                    print("Waiting for ask me later button")
                    ask_me_later_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH,"(.//input[@class='btn-link'])[1]")    
                    ))
                    ask_me_later_button.click()
                except TimeoutException:
                    print("Ask me later not found, proceeding")
                    
        except TimeoutException:
            print("An error occurred during the sign-in process.")
            self.driver.save_screenshot("debug_sign_in_error.png")
            raise

    def go_to_problem(self, question, solution):
        # Go to problem set page a
        self.driver.get(self.PROBLEMSET_URL)

        # Search the problem
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//input[@placeholder='Search questions']")))
        search_bar.send_keys(question)
        time.sleep(3)

        # Click on the problem link
        problem_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(.//div[@class='truncate']/a[@href])[2]"))).get_attribute('href')
        self.driver.get(problem_link)

        # Check if it is a premium question
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[contains(@class,'mb-4') and contains(text(), 'Subscribe to unlock.')]")))
            print("Premium question found. Exiting the function")
            return
        except TimeoutException:
            pass

        self.paste_the_code(solution)

    def paste_the_code(self, solution):
        try:
            # Click on languages and select the given language
            print("Clicked on the language button")
            languages_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, ".//div[contains(@class,'popover')]//button[contains(@class,'rounded items')]")))
            languages_button.click()

            print("Selected the language")
            language_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//div[@class='relative p-2 rounded-lg']//div[contains(text(),'{self.language}')]")))
            language_button.click()

            # Get the code editor element and paste the solution
            editor_text = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(.//textarea[@class='inputarea monaco-mouse-cursor-text'])[1]")))
            editor_text.click()
            editor_text.send_keys(Keys.CONTROL + 'a')
            editor_text.send_keys(Keys.BACKSPACE)
            pyperclip.copy(solution)
            editor_text.send_keys(Keys.CONTROL, 'v')
            print("Solution pasted")

            # Click on submit button
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//button[@data-e2e-locator='console-submit-button']")))
            submit_button.click()
            print("Submitted the code")
            self.check_accepted_status()
            
        except:
            self.ui_instance.status = (
            "Execution failed due to one of the following reasons:\n"
            "1) Invalid credentials.\n"
            "2) Unable to log in directly through GitHub.\n"
            "3) GitHub login with Multi-Factor Authentication (MFA) enabled.\n"
            "4) Execution interrupted by an unexpected event.\n"
            "5) Google Chrome browser is not installed on this device.\n"
            "6) This device does not meet the system requirements to run the bot application.\n"
            "7) The account has not been authenticated on this device at least once.")
             
    def check_login_status(self):
        try:
            problem_link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, ".//a[@href='/problemset/all/']")))
            problem_link.click()
            print("Successfull login")
        except:
            print("Unsuccessful login")
            self.ui_instance.status = (
            "Execution failed due to one of the following reasons:\n"
            "1) Invalid credentials.\n"
            "2) Unable to log in directly through GitHub.\n"
            "3) GitHub login with Multi-Factor Authentication (MFA) enabled.\n"
            "4) Execution interrupted by an unexpected event.\n"
            "5) Google Chrome browser is not installed on this device.\n"
            "6) This device does not meet the system requirements to run the bot application.\n"
            "7) The account has not been authenticated on this device at least once.")
            self.cleanup()
            
    def check_accepted_status(self):
        try:
            accepted_visual = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH,".//span[contains(@data-e2e-locator, 'submission-result') and text()='Accepted']")))
            if accepted_visual.is_displayed():
                pass
            else:
                time.sleep(10)
        except:
            print("Solution not accepted") 
    
    def cleanup(self):
        if self.driver:
            pyperclip.copy("")
            self.driver.quit()
            print("Closed browser")
            
    def language_file_selector(self):
        file_name = ""
        if self.language == "Python3":
            file_name = python_json_data
        if self.language == "Java":
            file_name = java_json_data
        if self.language == "C++":
            file_name = cplus_json_data
        if self.language == "JavaScript":
            file_name = javascript_json_data
        return file_name
             
    def run(self):
        try:
            # Initialize Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--window-position=-2000,0")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(self.LOGIN_URL)

            # Sign in
            self.sign_in()
            
            # Check success login or not 
            self.check_login_status()

            # Specify the file name
            file_name = self.language_file_selector()

            count_questions = self.questions 
            for problem_title, code_snippet in file_name.items():
                if count_questions != 0:
                    self.go_to_problem(problem_title, code_snippet)
                else:
                    break
                count_questions -= 1   
            self.ui_instance.status = "Execution successful!"
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    bot = LeetCodeBot("abc@gmail.com", "123", "Python3", 1)
    bot.run()

