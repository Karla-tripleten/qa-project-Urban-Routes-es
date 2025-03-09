import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
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
    button_taxi = (By.CSS_SELECTOR, '.button.round')
    button_comfort = (By.XPATH, "//div[@class='tcard-title'][text()='Comfort']")
    phone_number_field = (By.XPATH, "//div[contains(text(), 'Número de teléfono')]")
    phone_number_popup_window = (By.XPATH, "//input[@id='phone']")
    button_next_phone_number_popup_window = (By.CSS_SELECTOR, ".button.full")
    code_field = (By.XPATH, "//label[contains(text(), 'Introduce el código')]")
    button_confirm = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_field = (By.CLASS_NAME, "pp-text")
    button_add_card = (By.XPATH, "//div[@class='pp-title' and contains(text(), 'Agregar tarjeta')]")
    number_card_field = (By.ID, 'number')
    code_card_field = (By.XPATH, "//input[@placeholder='12']")
    button_add_in_popup_window = (By.XPATH, "//button[@type='submit' and contains(text(), 'Agregar')]")
    button_close_add_payment_window= (By.XPATH, "(//button[@class= 'close-button section-close'])[3]")
    popup_window_add_card = (By.CLASS_NAME, "card-wrapper")
    message_to_driver_field = (By.ID, "comment")
    left_window = (By.CSS_SELECTOR, ".workflow-subcontainer")


    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def set_from(self, from_address): #Codigo para rellenar el campo "Desde"
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address): #Codigo para rellenar el campo "Hasta"
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self): #Codigo para encontrar el campo "Desde"
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self): #Codigo para encontrar el campo "Hasta"
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route (self, from_address, to_address): #Código para colocar la ruta en los campos "Desde" y "Hasta"
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_button_taxi (self): #Codigo para obtener el botón "Pedir un taxi"
        return WebDriverWait (self.driver, 10).until(
            EC.element_to_be_clickable(self.button_taxi)
        )

    def click_on_button_taxi (self): #Codigo para dar click en el botón "Pedir un taxi"
        self.get_request_button_taxi().click()

    def get_button_comfort (self): #Codigo para obtener el botón "Comfort"
        return WebDriverWait (self.driver, 10).until(
            EC.element_to_be_clickable(self.button_comfort)
        )

    def click_on_button_comfort (self): #Codigo para dar click al botón comfort
        self.get_button_comfort().click()

    def get_phone_number_field (self): #Código para obtener el campo de insertar número
        return WebDriverWait (self.driver, 20).until(
            EC.element_to_be_clickable(self.phone_number_field)
        )

    def click_phone_number_field (self): #Código para dar click al campo de insertar número
        self.get_phone_number_field().click()

    def set_phone_number_popup_window (self): #Código para ingresar el número en la ventana de "Insertar número"
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located(self.phone_number_popup_window)
        )
        WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(self.phone_number_popup_window)
        ).send_keys(data.phone_number)

    def click_button_next_phone_number_popup_window (self): #Código para dar click al botón "Siguiente" del formulario ingresar número
        WebDriverWait (self.driver,10).until(
            EC.element_to_be_clickable(self.button_next_phone_number_popup_window)
        ).click()

    def get_code_field (self): #Código para obtener el campo "Código"
        return self.driver.find_element(*self.code_field)

    def click_code_field (self): #Código para dar click al campo código
        WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(self.code_field)
        ).click()

    def enter_code_field(self):
        code = retrieve_phone_code(self.driver)
        code_field_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.code_field)
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", code_field_element,
                                   code)  # Ingresar el código usando JavaScript

    def click_button_confirm (self): #Código para dar click al botón confirmar del formulario "Insertar número de teléfono"
        self.driver.find_element(*self.button_confirm).click()

    def get_payment_method_field (self): #Código para obtener el campo "Metodo de pago"
        return self.driver.find_element(*self.payment_method_field)

    def click_on_payment_method_field (self): #Código para dar click al campo de "Metodo de pago"
        self.driver.find_element(*self.payment_method_field).click()

    def click_on_button_add_card (self): #Código para dar click en el botón de "Agregar tarjeta"
        self.driver.find_element(*self.button_add_card).click()

    def click_on_number_card_field (self): #Código para dar click al campo para agregar el número de tarjeta
        self.driver.find_element(*self.number_card_field).click()

    def add_number_card (self): #Código para añadir el número de tarjeta
        self.driver.find_element(*self.number_card_field).send_keys(data.card_number)

    def get_code_card_field (self): #Código para obtener el campo código de tarjeta
        return self.driver.find_element(*self.code_card_field)

    def click_on_code_card_field (self): #Código para dar click al campo Código
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.code_card_field)
        ).click()

    def enter_code_card (self,code_card_field): #Código para agregar el código de tarjeta
        WebDriverWait(self.driver,30).until(
            EC.element_to_be_clickable(self.code_card_field)
        ).send_keys(data.card_code)

    def get_button_add_popup_window (self): #Código para obtener el botón "Agregar" del formulario para agregar tarjeta
        return self.driver.find_element(*self.button_add_in_popup_window)

    def click_on_button_add_popup_window (self): #Código para dar click al botón "Agregar" del formulario para agregar tarjeta
        WebDriverWait(self.driver,20).until(
            EC.element_to_be_clickable(self.popup_window_add_card)
        ).click()

        WebDriverWait(self.driver,20).until(
            EC.element_to_be_clickable(self.button_add_in_popup_window)
        ).click()

    def get_button_close_add_payment_window (self): #Código para obtener el botón "Cerrar" de la ventana para agregar el metodo de pago
        return self.driver.find_element(*self.button_close_add_payment_window)

    def click_on_button_close_add_payment_window (self):
        WebDriverWait(self.driver,20).until(
            EC.element_to_be_clickable(self.button_close_add_payment_window)
        ).click()

    def get_message_to_driver_field (self): #Código para obtener el campo "Mensaje para el conductor"
        return WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(self.message_to_driver_field)
        )

    def click_message_to_driver_field (self): #Código para dar click en el campo "Mensaje al conductor"
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.message_to_driver_field)
        ).click()








class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options ()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_rate (self): #Prueba para seleccionar la tárifa comfort
        self.test_set_route()
        routes_page = UrbanRoutesPage (self.driver)
        routes_page.click_on_button_taxi()
        routes_page.click_on_button_comfort()

    def test_set_phone_number (self):
        self.test_select_comfort_rate()
        routes_page = UrbanRoutesPage (self.driver)
        routes_page.click_phone_number_field()
        routes_page.set_phone_number_popup_window()
        routes_page.click_button_next_phone_number_popup_window()
        routes_page.click_code_field()
        routes_page.enter_code_field()
        routes_page.click_button_confirm()

    def test_set_select_payment_method (self):
        self.test_select_comfort_rate()
        routes_page = UrbanRoutesPage (self.driver)
        routes_page.click_on_payment_method_field()
        routes_page.click_on_button_add_card()
        routes_page.click_on_number_card_field()
        routes_page.add_number_card()
        routes_page.click_on_code_card_field()
        routes_page.enter_code_card(routes_page.code_card_field)
        routes_page.click_on_button_add_popup_window()
        routes_page.click_on_button_close_add_payment_window()

    def test_message_to_driver (self): #Código para insertar mensaje al conductor
        self.test_select_comfort_rate()
        routes_page = UrbanRoutesPage (self.driver)
        routes_page.click_message_to_driver_field()

















    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
