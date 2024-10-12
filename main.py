from resources import data, selector
from selenium import webdriver
from util import retrieve_phone_code_page, UrbanRoutesPage


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
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        address_from = data.address_from
        address_to = data.address_to

        routes_page.wait_for_element(selector.initial_page)
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_rate(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)
        routes_page.wait_for_element(selector.button_ask_taxi)
        routes_page.button_ask_for_a_taxi()
        routes_page.button_comfort()

        assert routes_page.get_rate() == "Comfort"

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        phone_number = data.phone_number
        routes_page.wait_for_element(selector.button_select_number)
        routes_page.button_phone_number()
        routes_page.set_phone_number(phone_number)

        assert routes_page.get_phone_number_button() == "Siguiente"

        routes_page.button_next()

    def test_fill_code_phone_number(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        try:
            confirmation_code = retrieve_phone_code_page.retrieve_phone_code(self.driver)
            routes_page.set_code(confirmation_code)
        except Exception as e:
            print(f"Error al recuperar el código: {e}")

        assert routes_page.get_button_confirm() == "Confirmar"

        routes_page.button_confirm()

    def test_fill_credit_card(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        card_code = data.card_code
        card_number = data.card_number

        routes_page.button_payment_method()
        routes_page.button_add_payment_method()
        routes_page.set_payment_method(card_number)
        routes_page.set_payment_method_code(card_code)
        routes_page.click_payment_method()

        assert routes_page.set_finish_payment_method() == "Agregar"

        routes_page.button_finish_payment_method()
        routes_page.button_end_payment_method()
        routes_page.move_element(selector.button_order_requirement)

    def test_send_message_for_driver(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        assert routes_page.get_message() == "Mensaje para el conductor..."

        message_driver = data.message_for_driver
        routes_page.write_message(message_driver)
        routes_page.wait_for_element(selector.add_ice_cream)

    def test_select_a_blanket_and_handkerchief(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        assert routes_page.get_text_blanket_and_handkerchief() == "Manta y pañuelos"

        routes_page.select_blanket_and_handkerchief()


    def test_ask_for_two_ice_creams(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        assert routes_page.get_text_ice_cream() == "Helado"

        routes_page.add_quantity_of_ice_cream(2)
        routes_page.reserve_a_taxi()

    def test_wait_for_the_taxi_confirmation(self):
        routes_page = UrbanRoutesPage.UrbanRoutes(self.driver)

        assert routes_page.get_last_modal() == "Buscar automóvil"
        routes_page.wait_for_element(selector.taxi_confirmation)

    @classmethod
    def teardown_class(cls):
         cls.driver.quit()