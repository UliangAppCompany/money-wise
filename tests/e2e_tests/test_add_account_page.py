import pytest 

from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 

pytestmark = [
    pytest.mark.django_db, 
    pytest.mark.usefixtures("register_new_user", "validate_new_user") 
]

def test_user_can_login_at_the_login_page(server, driver):
    driver.get(f"{server.live_server_url}/login")

    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("john@example.com")

    password_input = driver.find_element(By.NAME, "password") 
    password_input.send_keys("password") 

    submit_button = driver.find_element(By.ID, "login-form-submit-button")
    submit_button.click()

    elem = WebDriverWait(driver, 60).until(expected_conditions
        .text_to_be_present_in_element((By.ID, "auth-message"), "Authenticated!"))

    assert elem is not None



def test_click_submit_and_continue_button_fires_api_post_request(driver): 
    pass


     