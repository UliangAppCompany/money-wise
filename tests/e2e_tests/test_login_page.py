import pytest 

from django.test import  override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 

from registration.service import create_user

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

@pytest.mark.django_db 
@override_settings(DEBUG=True)
class TestSetPasswordPage(StaticLiveServerTestCase): 

    @classmethod 
    def setUpClass(cls) -> None:
        super().setUpClass()
        if (path:=settings.CHROMEDRIVER_PATH): 
            cls.driver = webdriver.Chrome(path)
        else: 
            cls.driver = webdriver.Chrome()
        User = get_user_model()
        User.objects.all().delete()
        cls.user = create_user('joe@example.com' ) 
        cls.user.is_validated = True
        cls.user.save()

    @classmethod 
    def tearDownClass(cls): 
        cls.driver.quit()
        super().tearDownClass()

    def test_change_password(self): 
        self.driver.get(f'{self.live_server_url}/user/{self.user.id}/set-password')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'retype_password').send_keys('password')

        self.driver.find_element(By.ID, 'submit-password-button').click() 

        elem = WebDriverWait(self.driver, 60).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'message-box'), 'Changed password!')
        )

        self.assertIsNotNone(elem)

    