

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Инициализация браузера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.saucedemo.com/")

print("Анализ стабильных селекторов для saucedemo.com")
print("=" * 60)

# Анализируем каждый элемент
elements = [
    ("Поле ввода логина", "user-name"),
    ("Поле ввода пароля", "password"),
    ("Кнопка Login", "login-button"),
    ("Контейнер с логотипом", "login_logo"),
    ("Контейнер с изображением бота", "bot_column"),
]

for element_name, element_id in elements:
    try:
        element = driver.find_element(By.ID, element_id)
        print(f" {element_name}:")
        print(f"  ID: {element_id}")
        print(f"  Найден: ДА")
        print(f"  Отображается: {element.is_displayed()}")
        
        # Проверяем альтернативные селекторы
        try:
            by_name = driver.find_element(By.NAME, element_id)
            print(f"  NAME: {element_id} ")
        except:
            print(f"  NAME: не найден ")
            
        try:
            by_data_test = driver.find_element(By.CSS_SELECTOR, f"[data-test='{element_id}']")
            print(f"  data-test='{element_id}' ")
        except:
            print(f"  data-test: не найден ")
            
    except:
        print(f" {element_name}: элемент не найден по ID '{element_id}'")
    
    print()

driver.quit()
print("Анализ завершен!")
