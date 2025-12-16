
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Важно импортировать By!
import time

print("=" * 60)
print("Лабораторная работа 3: Тест страницы логина")
print("=" * 60)

try:
    # 1. Указываем путь к драйверу
    driver_path = r'D:\вм\laba3\chromedriver.exe'
    print(f"Используется драйвер: {driver_path}")
    
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    print(" Браузер успешно запущен")
    
    # 2. Открываем страницу
    driver.get("https://www.saucedemo.com/")
    print(f" Страница открыта: {driver.title}")
    
    # 3. Анализ стабильных селекторов (ВАЖНО: используем By.ID, а не строку "ID")
    print("\n[Анализ стабильных селекторов]:")
    
    # Проверяем каждый элемент
    elements_to_check = [
        ("Поле логина", "user-name"),
        ("Поле пароля", "password"),
        ("Кнопка входа", "login-button")
    ]
    
    for element_name, element_id in elements_to_check:
        try:
            element = driver.find_element(By.ID, element_id)
            print(f"  {element_name}: id='{element_id}' -  найден")
        except:
            print(f"  {element_name}: id='{element_id}' -  не найден")
    
    # 4. Тест: вход с валидными данными
    print("\n[Тест: вход с валидными данными]")
    
    # Вводим данные
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    
    # 5. Проверка успешного входа
    current_url = driver.current_url
    if "inventory.html" in current_url:
        print(" ТЕСТ ПРОЙДЕН! Пользователь успешно вошел в систему.")
        
        # Дополнительная проверка
        try:
            menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
            if menu_button.is_displayed():
                print(" Найдена кнопка меню (дополнительное подтверждение)")
        except:
            print(" Кнопка меню не найдена, но вход выполнен")
        
        result = "УСПЕХ"
    else:
        print(f" Тест не пройден. Текущий URL: {current_url}")
        result = "НЕУДАЧА"
       
    # 7. Закрываем браузер
    driver.quit()
    print(" Браузер закрыт")
    
    print("\n" + "=" * 60)
    print(f"ИТОГ:  {result}")
    print("=" * 60)
    
except Exception as e:
    print(f"\n ОШИБКА: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

    
#Запуск: python lab3_correct.py 