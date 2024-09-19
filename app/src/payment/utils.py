from typing import final
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from payment.models import ScreenshotPath


import os
class RakBankManager:

    def __init__(self, payment_link, personal_info, payment_method):
        self.payment_link = payment_link
        self.personal_info = personal_info
        self.payment_method = payment_method
        self.driver = None  # WebDriver instance

    def initialize_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            # options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options,service=Service())
            self.driver=webdriver.Chrome(options=options,
                                    service=Service(ChromeDriverManager().install()),
            )
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def open_page(self, url):
        self.driver.get(url)

    def enter_name(self, name):
        try:
            self.driver.switch_to.frame("simplify-checkout-frame")
            name_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            name_input.send_keys(name)
        except Exception as e:
            print(f"Error entering name: {e}")

    def enter_email(self, email):
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "email"))
            )
            email_input.send_keys(email)
        except Exception as e:
            print(f"Error entering email: {e}")

    def enter_address(self, address):
        try:
            address_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "address"))
            )
            address_input.send_keys(address)
        except Exception as e:
            print(f"Error entering address: {e}")

    def enter_city(self, city):
        try:
            city_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "city"))
            )
            city_input.send_keys(city)
        except Exception as e:
            print(f"Error entering city: {e}")

    def enter_card_number(self, card_number):
        try:
            card_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cc-number"))
            )
            card_input.send_keys(card_number)
        except Exception as e:
            print(f"Error entering card number: {e}")

    def enter_expiry_date(self, expiry_date):
        try:
            expiry_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "expiryMonthYear"))
            )
            expiry_input.send_keys(expiry_date)
        except Exception as e:
            print(f"Error entering expiry date: {e}")

    def enter_cvv(self, cvv):
        try:
            cvv_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cc-cvc"))
            )
            cvv_input.send_keys(cvv)
        except Exception as e:
            print(f"Error entering CVV: {e}")

    def click_button_by_class(self, class_name):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            button = self.driver.find_element(By.CLASS_NAME, class_name)
            button.click()
        except Exception as e:
            print(f"Error clicking button by class: {e}")

    def click_button_by_id(self, element_id):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            button = self.driver.find_element(By.ID, element_id)
            button.click()
        except Exception as e:
            print(f"Error clicking button by ID: {e}")

    def automate_payment(self):
        # Open payment page
        self.initialize_driver()
        try:
            self.open_page(self.payment_link.url)

            # Accept cookies and start payment
            self.click_button_by_id("onetrust-accept-btn-handler")
            self.click_button_by_id("payInvoiceButton")

            # Fill in payment form
            self.enter_name(self.personal_info.name)
            self.enter_email(self.personal_info.email)
            self.enter_address(self.personal_info.address)
            self.enter_city(self.personal_info.city)

            # Submit the form
            self.click_button_by_class("btn-order")

            # Fill in card details
            self.enter_card_number(self.payment_method.card_number)
            self.enter_expiry_date(self.payment_method.expiry_date)
            self.enter_cvv(self.payment_method.cvv)

            # Finalize payment
            self.click_button_by_class("btn-order")

            screenshot_path_obj = ScreenshotPath.objects.first()
            screenshot_path = screenshot_path_obj.path if screenshot_path_obj else "/default/path/"

            screenshot_file = f"{screenshot_path}/{self.payment_link.short_name}_payment_automation_result.png"
            self.driver.save_screenshot(screenshot_file)
        finally:
            self.close_driver()
