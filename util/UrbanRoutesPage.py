from resources import selector
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class UrbanRoutes:

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*selector.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*selector.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*selector.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*selector.to_field).get_property('value')


    def wait_for_element(self, locator, timeout=40):
        WebDriverWait(self.driver,timeout).until(expected_conditions.visibility_of_element_located(locator))

    def button_ask_for_a_taxi(self):
        self.driver.find_element(*selector.button_ask_taxi).click()

    def button_comfort(self):
        self.driver.find_element(*selector.button_select_comfort).click()

    def get_rate(self):
        return self.driver.find_element(*selector.button_select_comfort).text

    def button_phone_number(self):
        self.driver.find_element(*selector.button_select_number).click()

    def set_phone_number(self,phone_number):
        self.driver.find_element(*selector.phone_number).send_keys(phone_number)

    def get_phone_number_button(self):
        return self.driver.find_element(*selector.button_phone_number_next).text

    def button_next(self):
        self.driver.find_element(*selector.button_phone_number_next).click()

    def set_code(self, code):
        self.driver.find_element(*selector.code).send_keys(code)

    def button_confirm(self):
        self.driver.find_element(*selector.confirm_code).click()

    def get_button_confirm(self):
        return self.driver.find_element(*selector.confirm_code).text

    def button_payment_method(self):
        self.driver.find_element(*selector.payment_method).click()

    def button_add_payment_method(self):
        self.driver.find_element(*selector.add_payment_method).click()

    def set_payment_method(self,card_number):
        self.driver.find_element(*selector.credit_card).send_keys(card_number)

    def set_payment_method_code(self,code_card_number):
        self.driver.find_element(*selector.code_credit_card).send_keys(code_card_number)

    def click_payment_method(self):
        self.driver.find_element(*selector.credit_card).click()

    def set_finish_payment_method(self):
        return self.driver.find_element(*selector.button_add_credit_card).text

    def button_finish_payment_method(self):
        self.driver.find_element(*selector.button_add_credit_card).click()

    def button_end_payment_method(self):
        self.driver.find_element(*selector.button_exit_add_payment_method).click()

    def move_element(self,element):
        element_to = self.driver.find_element(*element)
        self.driver.execute_script("arguments[0].scrollIntoView();", element_to)

    def get_message(self):
        return self.driver.find_element(*selector.label_comment).text

    def write_message(self, message):
        self.driver.find_element(*selector.comment).send_keys(message)

    def get_text_blanket_and_handkerchief(self):
        return self.driver.find_element(*selector.label_blanket_and_handkerchief).text

    def select_blanket_and_handkerchief(self):
        self.driver.find_element(*selector.blanket_and_handkerchief).click()

    def get_text_ice_cream(self):
        return self.driver.find_element(*selector.label_ice_cream).text

    def add_quantity_of_ice_cream(self,quantity):
        for _ in range(quantity):
            self.driver.find_element(*selector.add_ice_cream).click()
    def reserve_a_taxi(self):
        self.driver.find_element(*selector.button_reserve).click()

    def get_last_modal(self):
        return self.driver.find_element(*selector.last_modal).text
