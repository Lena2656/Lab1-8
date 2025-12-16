
class Calculator:
    """Класс калькулятора с базовыми математическими операциями."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Сложение двух чисел."""
        return a + b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Деление двух чисел.
        
        Raises:
            ZeroDivisionError: при попытке деления на ноль
        """
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b
    
    @staticmethod
    def is_prime_number(n: int) -> bool:
        """Проверка, является ли число простым.
        
        Простое число - натуральное число больше 1,
        которое делится только на 1 и на само себя.
        """
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Проверяем делители до квадратного корня из n
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True