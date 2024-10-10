import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
import json
import time
from selenium.common import WebDriverException

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""


    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    initial_page = (By.ID, 'to')
    button_ask_taxi = (By.CSS_SELECTOR, ".button.round")
    button_select_comfort = (By.CSS_SELECTOR, ".tcard.active")
    button_select_number = (By.CSS_SELECTOR, ".np-button")
    phone_number = (By.CSS_SELECTOR, ".input#phone.input")
    code = (By.CSS_SELECTOR, "#code.input")
    button_next = (By.XPATH, "//button[@type='submit' and @class='button full' and text()='Siguiente']")
    confirm_code = (By.XPATH, "//button[@type='submit' and @class='button full' and text()='Confirmar']")
    payment_method = (By.CSS_SELECTOR, ".pp-button.filled")
    add_payment_method = (By.CSS_SELECTOR, ".pp-plus-container")
    credit_card= (By.ID, "number")
    code_credit_card= (By.CSS_SELECTOR, "input.card-input#code")
    button_add_credit_card= (By.XPATH, "//button[@type='submit' and @class='button full' and text()='Agregar']")
    button_exit_add_payment_method = (By.CSS_SELECTOR,"div.payment-picker.open div.modal div.section.active button.close-button.section-close")
    button_order_requirement = (By.CSS_SELECTOR,".reqs-header")
    button_ice_cream = (By.CSS_SELECTOR,"div.r-link")
    comment = (By.CSS_SELECTOR,"input#comment")
    blanket_and_handkerchief = (By.CSS_SELECTOR,"span.slider.round")
    add_ice_cream = (By.CSS_SELECTOR,"div.counter-plus")
    button_reserve = (By.CSS_SELECTOR,"button.smart-button")
    taxi_confirmation = (By.CSS_SELECTOR, "div.order-btn-group div.order-button")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def wait_for_element(self, locator, timeout=80):
        WebDriverWait(self.driver,timeout).until(expected_conditions.visibility_of_element_located(locator))

    def button_ask_for_a_taxi(self):
        self.driver.find_element(*self.button_ask_taxi).click()

    def button_comfort(self):
        self.driver.find_element(*self.button_select_comfort).click()

    def button_phone_number(self):
        self.driver.find_element(*self.button_select_number).click()

    def set_phone_number(self,phone_number):
        self.driver.find_element(*self.phone_number).send_keys(phone_number)

    def button_next(self):
        self.driver.find_element(*self.button_number_next).click()

    def set_code(self, code):
        self.driver.find_element(*self.code).send_keys(code)

    def button_confirm(self):
        self.driver.find_element(*self.confirm_code).click()

    def button_payment_method(self):
        self.driver.find_element(*self.payment_method).click()

    def button_add_payment_method(self):
        self.driver.find_element(*self.add_payment_method).click()

    def set_payment_method(self,card_number):
        self.driver.find_element(*self.credit_card).send_keys(card_number)

    def set_payment_method_code(self,code_card_number):
        self.driver.find_element(*self.code_credit_card).send_keys(code_card_number)

    def click_payment_method(self):
        self.driver.find_element(*self.credit_card).click()

    def button_finish_payment_method(self):
        self.driver.find_element(*self.button_add_credit_card).click()

    def button_end_payment_method(self):
        self.driver.find_element(*self.button_exit_add_payment_method).click()

    def move_element(self,element):
        element_to = self.driver.find_element(*element)
        self.driver.execute_script("arguments[0].scrollIntoView();", element_to)

    def button_order_requirements(self):
        self.driver.find_element(*self.button_order_requirement).click()

    def write_message(self):
        self.driver.find_element(*self.comment).send_keys("Hola conductor")

    def select_blanket_and_handkerchief(self):
        self.driver.find_element(*self.blanket_and_handkerchief).click()

    def button_open_box_ice_cream(self):
        self.driver.find_element(*self.button_ice_cream).click()

    def add_quantity_of_ice_cream(self,quantity):
        for _ in range(quantity):
            self.driver.find_element(*self.add_ice_cream).click()
    def reserve_a_taxi(self):
        self.driver.find_element(*self.button_reserve).click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_code = data.card_code

        #configurate address
        routes_page.wait_for_element(routes_page.initial_page)
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        #select comfort rate
        routes_page.wait_for_element(routes_page.button_ask_taxi)
        routes_page.button_ask_for_a_taxi()
        routes_page.button_comfort()

        # fill phonenumber
        routes_page.wait_for_element(routes_page.button_select_number)
        routes_page.button_phone_number()
        routes_page.set_phone_number(phone_number)
        routes_page.button_next()

        # fill code phonenumber
        try:
            confirmation_code = retrieve_phone_code(self.driver)
            routes_page.set_code(confirmation_code)
        except Exception as e:
            print(f"Error al recuperar el código: {e}")

        routes_page.button_confirm()

        # fill credit card
        routes_page.button_payment_method()
        routes_page.button_add_payment_method()
        routes_page.set_payment_method(phone_number)
        routes_page.set_payment_method_code(card_code)
        routes_page.click_payment_method()
        routes_page.button_finish_payment_method()
        routes_page.button_end_payment_method()
        routes_page.move_element(routes_page.button_order_requirement)
        routes_page.button_order_requirements()

        # write a message for the driver
        routes_page.write_message()
        routes_page.move_element(routes_page.button_ice_cream)
        routes_page.button_open_box_ice_cream()
        routes_page.wait_for_element(routes_page.add_ice_cream)

        # select a blanket and a handkerchief
        routes_page.select_blanket_and_handkerchief()

        # ask for 2 ice creams
        routes_page.add_quantity_of_ice_cream(2)
        routes_page.reserve_a_taxi()

        #wait for the taxi confirmation / last modal
        routes_page.wait_for_element(routes_page.taxi_confirmation)

    @classmethod
    def teardown_class(cls):
         cls.driver.quit()