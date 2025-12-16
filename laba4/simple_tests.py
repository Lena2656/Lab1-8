from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time

class SimpleFormTests:
    """Класс для тестирования простой формы"""
    
    def __init__(self):
        """Инициализация браузера"""
        print("=" * 50)
        print("Лабораторная работа 4: Тестирование формы")
        print("=" * 50)
        
        # Создаем путь к локальному файлу
        self.form_path = os.path.abspath("simple_form.html")
        
        # 1. ЯВНЫЙ ПУТЬ К ДРАЙВЕРУ (как в laba3)
        driver_path = r'D:\вм\laba4\chromedriver.exe'
        print(f"Используется драйвер: {driver_path}")
        
        # Проверяем наличие файла
        if not os.path.exists(driver_path):
            print(f"✗ Файл драйвера не найден: {driver_path}")
            print("Скачайте chromedriver.exe с https://chromedriver.chromium.org/")
            print("и поместите в папку D:\\вм\\laba4\\")
            exit(1)
        
        # 2. Используем явный путь к драйверу
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        
        print(f" Браузер успешно запущен")
        print(f"Форма: file://{self.form_path}")
    
    def open_form(self):
        """Открыть форму"""
        self.driver.get(f"file://{self.form_path}")
        time.sleep(2)
        print(" Форма открыта")
    
    def fill_field(self, field_id, value):
        """Заполнить поле"""
        try:
            field = self.driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(value)
            print(f" Заполнено поле {field_id}: {value}")
        except Exception as e:
            print(f" Ошибка при заполнении поля {field_id}: {e}")
    
    def click_submit(self):
        """Нажать кнопку отправки"""
        try:
            button = self.driver.find_element(By.TAG_NAME, "button")
            button.click()
            time.sleep(1)
            print(" Кнопка 'Отправить' нажата")
        except Exception as e:
            print(f" Ошибка при нажатии кнопки: {e}")
    
    def check_error_message(self, field_id):
        """Проверить сообщение об ошибке"""
        try:
            error_element = self.driver.find_element(By.ID, f"{field_id}Error")
            error_text = error_element.text
            is_displayed = bool(error_text)
            
            if is_displayed:
                print(f" Найдена ошибка для {field_id}: '{error_text}'")
            else:
                print(f" Ошибки для {field_id} нет")
            
            return is_displayed, error_text
        except:
            print(f" Не удалось проверить ошибку для {field_id}")
            return False, ""
    
    def check_success_message(self):
        """Проверить сообщение об успехе"""
        try:
            success_element = self.driver.find_element(By.ID, "successMessage")
            is_displayed = success_element.is_displayed()
            
            if is_displayed:
                print(" Сообщение об успехе: 'Форма успешно отправлена!'")
            else:
                print(" Сообщение об успехе не отображается")
            
            return is_displayed
        except:
            print(" Не удалось проверить сообщение об успехе")
            return False
    
    def take_screenshot(self, test_name):
        """Сделать скриншот"""
        try:
            filename = f"test_{test_name}_{time.strftime('%H%M%S')}.png"
            self.driver.save_screenshot(filename)
            print(f" Скриншот сохранен: {filename}")
        except:
            print(" Не удалось сохранить скриншот")
    
    def test_positive_scenario(self):
        """Позитивный тест: все поля валидны"""
        print("\n" + "=" * 50)
        print("Тест 1: Позитивный сценарий (все поля валидны)")
        print("=" * 50)
        
        self.open_form()
        
        # Заполняем все поля валидными данными
        self.fill_field("name", "Иван Иванов")
        self.fill_field("email", "ivan@example.com")
        self.fill_field("phone", "79991234567")
        self.fill_field("message", "Тестовое сообщение для проверки формы, содержащее более 10 символов.")
        
        # Отправляем форму
        self.click_submit()
        time.sleep(1)  # Даем время для обработки
        
        # Проверяем успешное сообщение
        success = self.check_success_message()
        
        # Проверяем, что нет ошибок
        errors = []
        for field in ["name", "email", "phone", "message"]:
            has_error, _ = self.check_error_message(field)
            if has_error:
                errors.append(field)
        
        if success and len(errors) == 0:
            print("\n ТЕСТ ПРОЙДЕН - форма успешно отправлена")
            self.take_screenshot("positive")
            return True
        else:
            print(f"\n ТЕСТ НЕ ПРОЙДЕН - ошибки в полях: {errors}")
            self.take_screenshot("positive_failed")
            return False
    
    def test_negative_scenario_empty_field(self):
        """Негативный тест: пустое обязательное поле"""
        print("\n" + "=" * 50)
        print("Тест 2: Негативный сценарий (пустое поле 'Имя')")
        print("=" * 50)
        
        self.open_form()
        
        # Заполняем все поля кроме имени
        self.fill_field("email", "test@example.com")
        self.fill_field("phone", "79991234567")
        self.fill_field("message", "Сообщение без имени")
        
        # Оставляем поле 'name' пустым
        self.fill_field("name", "")  # Очищаем поле
        
        # Отправляем форму
        self.click_submit()
        time.sleep(1)
        
        # Проверяем ошибку для поля 'name'
        has_error, error_text = self.check_error_message("name")
        
        # Проверяем, что нет успешного сообщения
        success = self.check_success_message()
        
        if has_error and not success and "Пожалуйста, введите имя" in error_text:
            print(f"\n ТЕСТ ПРОЙДЕН - получена ожидаемая ошибка: '{error_text}'")
            self.take_screenshot("negative_empty_name")
            return True
        else:
            print(f"\n ТЕСТ НЕ ПРОЙДЕН")
            print(f"  - Ошибка получена: {has_error}")
            print(f"  - Текст ошибки: '{error_text}'")
            print(f"  - Успешное сообщение показано: {success}")
            self.take_screenshot("negative_empty_name_failed")
            return False
    
    def test_negative_scenario_invalid_email(self):
        """Негативный тест: невалидный email"""
        print("\n" + "=" * 50)
        print("Тест 3: Негативный сценарий (невалидный email)")
        print("=" * 50)
        
        self.open_form()
        
        # Заполняем все поля
        self.fill_field("name", "Петр Петров")
        self.fill_field("email", "неправильный-email")  # Неправильный email
        self.fill_field("phone", "79991234567")
        self.fill_field("message", "Сообщение с неправильным email")
        
        # Отправляем форму
        self.click_submit()
        time.sleep(1)
        
        # Проверяем ошибку для email
        has_error, error_text = self.check_error_message("email")
        
        if has_error and "Введите корректный email" in error_text:
            print(f"\n ТЕСТ ПРОЙДЕН - получена ожидаемая ошибка: '{error_text}'")
            self.take_screenshot("negative_invalid_email")
            return True
        else:
            print(f"\n ТЕСТ НЕ ПРОЙДЕН")
            print(f"  - Ошибка получена: {has_error}")
            print(f"  - Текст ошибки: '{error_text}'")
            self.take_screenshot("negative_invalid_email_failed")
            return False
    
    def test_negative_scenario_invalid_phone(self):
        """Негативный тест: невалидный телефон"""
        print("\n" + "=" * 50)
        print("Тест 4: Негативный сценарий (невалидный телефон)")
        print("=" * 50)
        
        self.open_form()
        
        # Заполняем все поля
        self.fill_field("name", "Анна Смирнова")
        self.fill_field("email", "anna@example.com")
        self.fill_field("phone", "123")  # Слишком короткий
        self.fill_field("message", "Сообщение с неправильным телефоном")
        
        # Отправляем форму
        self.click_submit()
        time.sleep(1)
        
        # Проверяем ошибку для телефона
        has_error, error_text = self.check_error_message("phone")
        
        if has_error and "Телефон должен содержать 10-11 цифр" in error_text:
            print(f"\n ТЕСТ ПРОЙДЕН - получена ожидаемая ошибка: '{error_text}'")
            self.take_screenshot("negative_invalid_phone")
            return True
        else:
            print(f"\n ТЕСТ НЕ ПРОЙДЕН")
            print(f"  - Ошибка получена: {has_error}")
            print(f"  - Текст ошибки: '{error_text}'")
            self.take_screenshot("negative_invalid_phone_failed")
            return False
    
    def close(self):
        """Закрыть браузер"""
        self.driver.quit()
        print("\n Браузер закрыт")

def create_decision_matrix():
    """Создать матрицу принятия решений"""
    print("\n" + "=" * 70)
    print("МАТРИЦА ПРИНЯТИЯ РЕШЕНИЙ ДЛЯ ПОЛЕЙ ФОРМЫ")
    print("=" * 70)
    
    matrix = [
        ["ID", "Поле", "Тестовые данные", "Ожидаемый результат", "Тип теста"],
        ["1", "Имя", "Пустое", "Ошибка: 'Пожалуйста, введите имя'", "Негативный"],
        ["2", "Имя", "'Иван Иванов'", "Принимается", "Позитивный"],
        ["3", "Email", "Пустое", "Ошибка: 'Пожалуйста, введите email'", "Негативный"],
        ["4", "Email", "'неправильный-email'", "Ошибка: 'Введите корректный email'", "Негативный"],
        ["5", "Email", "'test@example.com'", "Принимается", "Позитивный"],
        ["6", "Телефон", "Пустое", "Принимается", "Позитивный"],
        ["7", "Телефон", "'123'", "Ошибка: 'Телефон должен содержать 10-11 цифр'", "Негативный"],
        ["8", "Телефон", "'79991234567'", "Принимается", "Позитивный"],
        ["9", "Сообщение", "Пустое", "Ошибка: 'Пожалуйста, введите сообщение'", "Негативный"],
        ["10", "Сообщение", "'Коротко'", "Ошибка (если < 10 символов)", "Негативный"],
        ["11", "Сообщение", "'Длинное сообщение более 10 символов'", "Принимается", "Позитивный"],
    ]
    
    # Вывод матрицы
    print(f"{'ID':<3} | {'Поле':<10} | {'Тестовые данные':<25} | {'Ожидаемый результат':<45} | {'Тип теста':<10}")
    print("-" * 100)
    
    for row in matrix[1:]:  # Пропускаем заголовок
        print(f"{row[0]:<3} | {row[1]:<10} | {row[2]:<25} | {row[3]:<45} | {row[4]:<10}")
    
    print("\n ПРИМЕЧАНИЯ:")
    print("• Поля 'Имя', 'Email', 'Сообщение' - обязательные")
    print("• Поле 'Телефон' - необязательное, но при заполнении должно быть 10-11 цифр")
    print("• Email должен содержать @ и домен (например, example.com)")
    print("• Телефон должен содержать только цифры, 10-11 символов")
    print("• Сообщение должно быть не пустым")

def main():
    """Главная функция"""
    tester = SimpleFormTests()
    
    results = []
    
    try:
        # Запускаем тесты
        results.append(("1. Позитивный тест (все поля валидны)", tester.test_positive_scenario()))
        results.append(("2. Негативный тест (пустое поле 'Имя')", tester.test_negative_scenario_empty_field()))
        results.append(("3. Негативный тест (невалидный email)", tester.test_negative_scenario_invalid_email()))
        results.append(("4. Негативный тест (невалидный телефон)", tester.test_negative_scenario_invalid_phone()))
        
        # Выводим итоги
        print("\n" + "=" * 60)
        print(" ИТОГИ ТЕСТИРОВАНИЯ")
        print("=" * 60)
        
        passed = 0
        failed_tests = []
        
        for test_name, result in results:
            status = " ПРОЙДЕН" if result else " НЕ ПРОЙДЕН"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
            else:
                failed_tests.append(test_name)
        
        print("\n" + "=" * 60)
        print(f" СТАТИСТИКА:")
        print(f"   Всего тестов: {len(results)}")
        print(f"   Пройдено: {passed}")
        print(f"   Не пройдено: {len(results) - passed}")
        
        if failed_tests:
            print(f"\n Не пройденные тесты: {', '.join(failed_tests)}")
        
        if passed == len(results):
            print("\n ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
        else:
            print(f"\n Процент успешных тестов: {passed/len(results)*100:.1f}%")
        
        # Создаем матрицу принятия решений
        create_decision_matrix()
        
    except Exception as e:
        print(f"\n ОШИБКА ВО ВРЕМЯ ТЕСТИРОВАНИЯ: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Закрываем браузер
        tester.close()

if __name__ == "__main__":
    main()

# Запуск: python simple_tests.py
