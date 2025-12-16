

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class SimpleLoginTest:
    def __init__(self):
        # Инициализация драйвера
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        print("Браузер инициализирован ")
    
    def test_valid_login(self):
        """Тест успешного входа"""
        print("\n--- Тест успешного входа ---")
        
        # 1. Открываем страницу
        self.driver.get("https://www.saucedemo.com/")
        print("Страница открыта ")
        
        # 2. Вводим логин
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")
        print("Логин введен ")
        
        # 3. Вводим пароль
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        print("Пароль введен ")
        
        # 4. Нажимаем кнопку входа
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        print("Кнопка нажата ")
        
        time.sleep(2)  # Ждем загрузки
        
        # 5. Проверяем успешный вход
        try:
            # Ищем элемент "Logout" в меню
            menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
            menu_button.click()
            time.sleep(1)
            
            logout_link = self.driver.find_element(By.ID, "logout_sidebar_link")
            
            if logout_link.is_displayed():
                print(" Успешный вход подтвержден! Элемент 'Logout' найден")
                return True
            else:
                print("  Элемент 'Logout' не отображается")
                return False
                
        except Exception as e:
            print(f" Ошибка: {e}")
            return False
    
    def test_invalid_login(self):
        """Тест неудачного входа с неверными данными"""
        print("\n--- Тест с неверными данными ---")
        
        # Открываем страницу снова
        self.driver.get("https://www.saucedemo.com/")
        
        # Вводим неверные данные
        self.driver.find_element(By.ID, "user-name").send_keys("wrong_user")
        self.driver.find_element(By.ID, "password").send_keys("wrong_password")
        self.driver.find_element(By.ID, "login-button").click()
        
        time.sleep(1)
        
        # Проверяем сообщение об ошибке
        try:
            error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            print(" Сообщение об ошибке появилось:", error_message.text[:50])
            return True
        except:
            print(" Сообщение об ошибке не появилось")
            return False
    
    def analyze_selectors(self):
        """Анализ стабильных селекторов"""
        print("\n--- Анализ стабильных селекторов ---")
        
        self.driver.get("https://www.saucedemo.com/")
        
        elements = [
            {"name": "Поле логина", "selectors": ["id='user-name'", "name='user-name'", "data-test='username'"]},
            {"name": "Поле пароля", "selectors": ["id='password'", "name='password'", "data-test='password'"]},
            {"name": "Кнопка входа", "selectors": ["id='login-button'", "name='login-button'", "data-test='login-button'"]},
        ]
        
        for element in elements:
            print(f"\n{element['name']}:")
            for selector in element['selectors']:
                try:
                    # Пробуем разные способы поиска
                    if selector.startswith("id="):
                        elem = self.driver.find_element(By.ID, selector.split("='")[1][:-1])
                    elif selector.startswith("name="):
                        elem = self.driver.find_element(By.NAME, selector.split("='")[1][:-1])
                    elif selector.startswith("data-test="):
                        elem = self.driver.find_element(By.CSS_SELECTOR, f"[{selector}]")
                    
                    print(f"   {selector} - найден")
                except:
                    print(f"   {selector} - не найден")
    
    def close(self):
        """Закрытие браузера"""
        self.driver.quit()
        print("\nБраузер закрыт ")

# Запуск тестов
if __name__ == "__main__":
    test = SimpleLoginTest()
    
    print("=" * 50)
    print("Лабораторная работа 3: Первые автотесты")
    print("=" * 50)
    
    # Анализ селекторов
    test.analyze_selectors()
    
    # Запуск тестов
    print("\n" + "=" * 50)
    print("Запуск автотестов")
    print("=" * 50)
    
    test_result1 = test.test_invalid_login()
    test_result2 = test.test_valid_login()
    
    # Итоги
    print("\n" + "=" * 50)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 50)
    print(f"Тест с неверными данными: {'ПРОЙДЕН' if test_result1 else 'НЕ ПРОЙДЕН'}")
    print(f"Тест успешного входа: {'ПРОЙДЕН' if test_result2 else 'НЕ ПРОЙДЕН'}")
    print(f"Общий результат: {'ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if test_result1 and test_result2 else 'ЕСТЬ ОШИБКИ'}")
    
    # Сохраняем скриншот результата
    test.driver.save_screenshot("test_result.png")
    print("Скриншот сохранен: test_result.png")
    
    test.close()

