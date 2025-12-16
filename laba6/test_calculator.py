import pytest
from calculator import Calculator


class TestCalculator:
    """Класс тестов для проверки функциональности Calculator."""
    
    # === ТЕСТИРОВАНИЕ МЕТОДА add() ===
    
    @pytest.mark.parametrize("a, b, expected", [
        # Базовые случаи
        (0, 0, 0),
        (1, 2, 3),
        
        # Отрицательные числа
        (-5, 10, 5),
        (-3, -7, -10),
        
        # Дробные числа
        (2.5, 3.5, 6.0),
        (0.1, 0.2, 0.3),
        
        # Большие числа
        (1000, 2000, 3000),
        
        # Граничные случаи
        (0, 100, 100),
        (-100, 0, -100),
    ])
    def test_add(self, a, b, expected):
        """Параметризованный тест метода сложения."""
        result = Calculator.add(a, b)
        # Используем approx для сравнения дробных чисел
        assert result == pytest.approx(expected), \
            f"Сложение {a} + {b} = {result}, ожидалось {expected}"
    
    # === ТЕСТИРОВАНИЕ МЕТОДА divide() ===
    
    @pytest.mark.parametrize("a, b, expected", [
        # Целочисленное деление
        (10, 2, 5),
        (9, 3, 3),
        
        # Деление дробных чисел
        (5.0, 2.0, 2.5),
        (1.0, 3.0, 1/3),
        
        # Деление отрицательных чисел
        (-10, 2, -5),
        (10, -2, -5),
        (-10, -2, 5),
        
        # Деление нуля
        (0, 5, 0),
        (0, -3.5, 0),
        
        # Деление на 1
        (7, 1, 7),
        (-3.14, 1, -3.14),
    ])
    def test_divide_normal_cases(self, a, b, expected):
        """Параметризованный тест метода деления (нормальные случаи)."""
        result = Calculator.divide(a, b)
        assert result == pytest.approx(expected), \
            f"Деление {a} / {b} = {result}, ожидалось {expected}"
    
    @pytest.mark.parametrize("a", [
        10,      # положительное число
        -5,      # отрицательное число
        0,       # ноль
        3.14,    # дробное число
    ])
    def test_divide_by_zero(self, a):
        """Параметризованный тест деления на ноль (проверка исключения)."""
        with pytest.raises(ZeroDivisionError) as exc_info:
            Calculator.divide(a, 0)
        
        # Проверка сообщения об ошибке
        assert str(exc_info.value) == "Деление на ноль невозможно"
    
    # === ТЕСТИРОВАНИЕ МЕТОДА is_prime_number() ===
    
    @pytest.mark.parametrize("n, expected", [
        # Простые числа (ожидается True)
        (2, True),
        (3, True),
        (5, True),
        (7, True),
        (11, True),
        (13, True),
        (17, True),
        (19, True),
        (23, True),
        (29, True),
        (31, True),
        (37, True),
        (41, True),
        (43, True),
        (47, True),
        
        # Не простые числа (ожидается False)
        (0, False),
        (1, False),
        (4, False),
        (6, False),
        (8, False),
        (9, False),
        (10, False),
        (12, False),
        (14, False),
        (15, False),
        
        # Отрицательные числа (не являются простыми)
        (-2, False),
        (-3, False),
        (-5, False),
        (-7, False),
        
        # Граничные случаи
        (997, True),  # простое число < 1000
        (1000, False), # составное число
    ])
    def test_is_prime_number(self, n, expected):
        """Параметризованный тест проверки числа на простоту."""
        result = Calculator.is_prime_number(n)
        assert result == expected, \
            f"Число {n}: ожидалось {expected}, получено {result}"
    
    # === ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ДЛЯ ДЕМОНСТРАЦИИ ===
    
    def test_add_commutative_property(self):
        """Дополнительный тест: проверка коммутативности сложения."""
        assert Calculator.add(5, 3) == Calculator.add(3, 5)
        assert Calculator.add(-2, 7) == Calculator.add(7, -2)
    
    def test_divide_identity_property(self):
        """Дополнительный тест: деление числа на само себя дает 1."""
        assert Calculator.divide(5, 5) == 1
        assert Calculator.divide(3.14, 3.14) == 1
    
    def test_prime_edge_cases(self):
        """Дополнительный тест: граничные случаи для простых чисел."""
        # Проверка больших простых чисел
        assert Calculator.is_prime_number(7919) == True  # простое число
        assert Calculator.is_prime_number(7921) == False # 89^2


# === ЗАПУСК ТЕСТОВ ПРИ НЕПОСРЕДСТВЕННОМ ВЫПОЛНЕНИИ ФАЙЛА ===
if __name__ == "__main__":
    print("Запуск модульных тестов Calculator...")
    print("=" * 50)
    
    # Простой ручной запуск без pytest (для демонстрации)
    test_calc = TestCalculator()
    
    # Проверка нескольких ключевых тестов
    print("1. Тестирование сложения:")
    test_calc.test_add(2, 3, 5)
    test_calc.test_add(-1, -1, -2)
    print("    Сложение работает корректно")
    
    print("\n2. Тестирование деления:")
    test_calc.test_divide_normal_cases(10, 2, 5)
    test_calc.test_divide_normal_cases(0, 5, 0)
    print("   Деление работает корректно")
    
    print("\n3. Тестирование деления на ноль:")
    try:
        Calculator.divide(10, 0)
        print("    ОШИБКА: Исключение не было вызвано!")
    except ZeroDivisionError as e:
        print(f"    Исключение перехвачено: {e}")
    
    print("\n4. Тестирование проверки простых чисел:")
    test_calc.test_is_prime_number(7, True)
    test_calc.test_is_prime_number(8, False)
    print("    Проверка простых чисел работает корректно")
    
    print("\n" + "=" * 50)
    print("Ручная проверка завершена. Для полного тестирования запустите:")
    print("  python -m pytest test_calculator.py -v")

# Запуск: python test_calculator.py
