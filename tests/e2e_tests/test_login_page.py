import pytest 

from django.test import  override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 

from registration.service import create_user

# pytestmark = [
#     pytest.mark.django_db, 
#     pytest.mark.usefixtures("register_new_user", "validate_new_user") 
# ]

@pytest.mark.django_db
@override_settings(DEBUG=True)
class TestLoginPage(StaticLiveServerTestCase): 

    @classmethod 
    def setUpClass(cls) -> None:
        super().setUpClass()
        if (path:=settings.CHROMEDRIVER_PATH): 
            cls.driver = webdriver.Chrome(path)
        else: 
            cls.driver = webdriver.Chrome()
        cls.user = create_user('joe@example.com' ) 
        cls.user.set_password('password', require_validation=False)
        cls.user.save()

    @classmethod 
    def tearDownClass(cls): 
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self): 
        self.driver.get(self.live_server_url + '/login') 

        self.driver.find_element(By.NAME, 'username').send_keys('joe@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password') 
        self.driver.find_element(By.ID, 'login-form-submit-button').click()

        self.assertIsNotNone(WebDriverWait(self.driver, 10).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'auth-message'), 'Authenticated!')
        ))