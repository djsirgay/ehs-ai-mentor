from dotenv import load_dotenv
load_dotenv()

from ai_mentor import AIMentor

def test_ai_mentor():
    mentor = AIMentor()
    
    # Тестовый протокол
    protocol = """
    НОВЫЙ ПРОТОКОЛ БЕЗОПАСНОСТИ - Работа с химическими веществами
    
    Все сотрудники, работающие с химическими веществами, должны:
    1. Знать основы обращения с опасными веществами
    2. Уметь читать паспорта безопасности (SDS)
    3. Знать процедуры при разливе химикатов
    4. Использовать соответствующие СИЗ
    
    Обязательно для лабораторных техников и исследователей.
    """
    
    # Тестируем на пользователе из лаборатории
    result = mentor.analyze_and_assign(protocol, "u001")
    
    print("Результат анализа:")
    print(f"Пользователь: {result['user_id']}")
    print(f"Решение AI: {result['analysis']}")
    print(f"Назначенные курсы: {result['assignments_made']}")

if __name__ == "__main__":
    test_ai_mentor()