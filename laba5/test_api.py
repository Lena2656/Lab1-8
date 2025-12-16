
import requests
import json

# Базовый URL API
BASE_URL = "https://jsonplaceholder.typicode.com"

# ТЕСТ 1: GET ЗАПРОС
def test_get_post():
    """GET запрос: получить пост"""
    print("Тест 1: GET запрос - получить пост")
    
    # Отправляем запрос
    response = requests.get(f"{BASE_URL}/posts/1")
    
    # Проверка статус кода
    assert response.status_code == 200, f"Статус код должен быть 200, получен {response.status_code}"
    
    # Преобразуем ответ в JSON
    data = response.json()
    
    # Проверка структуры JSON
    assert "id" in data, "В ответе должно быть поле 'id'"
    assert "userId" in data, "В ответе должно быть поле 'userId'"
    assert "title" in data, "В ответе должно быть поле 'title'"
    assert "body" in data, "В ответе должно быть поле 'body'"
    
    # Проверка значений полей
    assert data["id"] == 1, f"ID должен быть 1, получен {data['id']}"
    assert isinstance(data["userId"], int), "userId должен быть числом"
    assert isinstance(data["title"], str), "title должен быть строкой"
    assert isinstance(data["body"], str), "body должен быть строкой"
    
    print(" Тест 1 пройден")

# ТЕСТ 2: POST ЗАПРОС
def test_create_post():
    """POST запрос: создать пост"""
    print("\nТест 2: POST запрос - создать пост")
    
    # Данные для создания поста
    new_post = {
        "title": "Тестовый пост",
        "body": "Это тестовый пост для проверки API",
        "userId": 1
    }
    
    # Отправляем запрос
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    
    # Проверка статус кода
    assert response.status_code == 201, f"Статус код должен быть 201, получен {response.status_code}"
    
    # Преобразуем ответ в JSON
    data = response.json()
    
    # Проверка структуры JSON
    assert "id" in data, "В ответе должно быть поле 'id'"
    assert "title" in data, "В ответе должно быть поле 'title'"
    assert "body" in data, "В ответе должно быть поле 'body'"
    assert "userId" in data, "В ответе должно быть поле 'userId'"
    
    # Проверка значений полей
    assert data["title"] == new_post["title"], f"Заголовок должен быть '{new_post['title']}', получен '{data['title']}'"
    assert data["body"] == new_post["body"], f"Текст должен быть '{new_post['body']}', получен '{data['body']}'"
    assert data["userId"] == new_post["userId"], f"userId должен быть {new_post['userId']}, получен {data['userId']}"
    
    print(" Тест 2 пройден")

# ТЕСТ 3: PUT ЗАПРОС 
def test_update_post():
    """PUT запрос: обновить пост"""
    print("\nТест 3: PUT запрос - обновить пост")
    
    # Данные для обновления
    update_data = {
        "id": 1,
        "title": "Обновленный заголовок",
        "body": "Обновленный текст поста",
        "userId": 1
    }
    
    # Отправляем запрос
    response = requests.put(f"{BASE_URL}/posts/1", json=update_data)
    
    # Проверка статус кода
    assert response.status_code == 200, f"Статус код должен быть 200, получен {response.status_code}"
    
    # Преобразуем ответ в JSON
    data = response.json()
    
    # Проверка структуры JSON
    assert "id" in data, "В ответе должно быть поле 'id'"
    assert "title" in data, "В ответе должно быть поле 'title'"
    assert "body" in data, "В ответе должно быть поле 'body'"
    assert "userId" in data, "В ответе должно быть поле 'userId'"
    
    # Проверка значений полей
    assert data["id"] == update_data["id"], f"ID должен быть {update_data['id']}, получен {data['id']}"
    assert data["title"] == update_data["title"], f"Заголовок должен быть '{update_data['title']}', получен '{data['title']}'"
    assert data["body"] == update_data["body"], f"Текст должен быть '{update_data['body']}', получен '{data['body']}'"
    assert data["userId"] == update_data["userId"], f"userId должен быть {update_data['userId']}, получен {data['userId']}"
    
    print(" Тест 3 пройден")

# ТЕСТ 4: GET запрос - получить список постов
def test_get_posts_list():
    """GET запрос: получить список постов"""
    print("\nТест 4: GET запрос - получить список постов")
    
    # Отправляем запрос
    response = requests.get(f"{BASE_URL}/posts")
    
    # Проверка статус кода
    assert response.status_code == 200, f"Статус код должен быть 200, получен {response.status_code}"
    
    # Преобразуем ответ в JSON
    data = response.json()
    
    # Проверка структуры JSON
    assert isinstance(data, list), "Ответ должен быть списком"
    
    # Проверка значений
    assert len(data) > 0, f"Список не должен быть пустым"
    
    # Проверка первого поста
    if len(data) > 0:
        first_post = data[0]
        assert "id" in first_post, "У поста должно быть поле 'id'"
        assert "title" in first_post, "У поста должно быть поле 'title'"
        assert "body" in first_post, "У поста должно быть поле 'body'"
        assert "userId" in first_post, "У поста должно быть поле 'userId'"
    
    print(" Тест 4 пройден")

#ТЕСТ 5: НЕГАТИВНЫЙ ТЕСТ 
def test_post_not_found():
    """Негативный тест: пост не найден"""
    print("\nТест 5: Негативный тест - пост не найден")
    
    # Отправляем запрос к несуществующему посту
    response = requests.get(f"{BASE_URL}/posts/9999")
    
    # Проверка статус кода - исправлено!
    assert response.status_code == 404, f"Статус код должен быть 404, получен {response.status_code}"
    
    print(" Тест 5 пройден")

# ========== ЗАПУСК ВСЕХ ТЕСТОВ ==========
if __name__ == "__main__":
    """Главная функция для запуска всех тестов"""
    
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА 5: АВТОТЕСТЫ REST API")
    print("API: https://jsonplaceholder.typicode.com/")
    print("=" * 60)
    
    # Список всех тестов
    tests = [
        test_get_post,
        test_create_post,
        test_update_post,
        test_get_posts_list,
        test_post_not_found
    ]
    
    # Результаты тестов
    results = []
    
    # Запускаем каждый тест
    for test in tests:
        try:
            test()
            results.append(True)
        except AssertionError as e:
            print(f"✗ Тест не пройден: {e}")
            results.append(False)
        except Exception as e:
            print(f" Ошибка при выполнении теста: {e}")
            results.append(False)
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Всего тестов: {total}")
    print(f"Пройдено: {passed}")
    print(f"Не пройдено: {total - passed}")
    
    if passed == total:
        print("\nВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n{total - passed} тестов не пройдено")
    
    print("=" * 60) 

    #Запуск: python test_api.py  