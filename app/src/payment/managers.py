from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from payment.interfaces import PaymentManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BasePaymentManager(PaymentManager):
    def initialize_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(
                options=options,
                service=Service(ChromeDriverManager().install()),
            )

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def open_page(self, url):
        """Open a webpage."""
        self.driver.get(url)

    def enter_text_by_id(self, field_id, value):
        """Enter text into a field identified by its ID."""
        try:
            input_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, field_id))
            )
            input_field.send_keys(value)
        except Exception as e:
            print(f"Error entering text in field '{field_id}': {e}")

    def click_button_by_class(self, class_name):
        """Click a button identified by its class name."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            button = self.driver.find_element(By.CLASS_NAME, class_name)
            button.click()
        except Exception as e:
            print(f"Error clicking button by class: {e}")

    def enter_text_by_name(self, field_name,value):
       try:
           self.driver.switch_to.frame("simplify-checkout-frame")
           name_input = WebDriverWait(self.driver, 10).until(
               EC.visibility_of_element_located((By.NAME, field_name))
           )
           name_input.send_keys(value)
       except Exception as e:
           print(f"Error entering name: {e}")

    def click_button_by_id(self, element_id):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            button = self.driver.find_element(By.ID, element_id)
            button.click()
        except Exception as e:
            print(f"Error clicking button by ID: {e}")
