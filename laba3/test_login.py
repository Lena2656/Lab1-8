

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestLoginPage:
    """Тесты для страницы логина saucedemo.com"""
    
    @pytest.fixture
    def driver(self):
        """Фикстура для инициализации браузера"""
        service = Service(executable_path=r'D:\вм\laba3\chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        yield driver
        driver.quit()
    
    def test_page_title(self, driver):
        """Проверка заголовка страницы"""
        assert "Swag Labs" in driver.title
        print("Заголовок страницы корректен")
    
    def test_login_form_exists(self, driver):
        """Проверка наличия формы логина"""
        # Проверяем наличие всех элементов формы
        assert driver.find_element(By.ID, "user-name").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()
        assert driver.find_element(By.ID, "login-button").is_displayed()
        print("Форма логина присутствует на странице")
    
    def test_successful_login(self, driver):
        """Тест успешного входа"""
        # Вводим валидные данные
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Проверяем успешный вход по URL
        assert "inventory.html" in driver.current_url
        print("Вход выполнен успешно")
    
    def test_failed_login(self, driver):
        """Тест неудачного входа"""
        # Вводим неверные данные
        driver.find_element(By.ID, "user-name").send_keys("wrong_user")
        driver.find_element(By.ID, "password").send_keys("wrong_password")
        driver.find_element(By.ID, "login-button").click()
        
        # Проверяем сообщение об ошибке
        error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_message.is_displayed()
        assert "Epic sadface" in error_message.text
        print("Сообщение об ошибке отображается корректно")

# Запуск: pytest test_login.py -v
