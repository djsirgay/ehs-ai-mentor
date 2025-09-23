from dotenv import load_dotenv
load_dotenv()

from bedrock_client import BedrockClient
import time

def test_bedrock():
    print("Тестирую подключение к Bedrock...")
    
    client = BedrockClient()
    
    test_prompt = "Нужны ли курсы по химической безопасности лабораторному технику? Ответь JSON: {\"should_assign\": true, \"recommended_courses\": [\"HAZCOM-1910.1200\"], \"reason\": \"краткое обоснование\"}"
    
    try:
        start_time = time.time()
        print("Отправляю запрос к Bedrock...")
        
        result = client.analyze_protocol(
            "Протокол работы с химикатами", 
            {"user_id": "u001", "role": "lab_tech", "department": "Chemistry", "completed_courses": []},
            []
        )
        
        end_time = time.time()
        print(f"Ответ получен за {end_time - start_time:.2f} секунд:")
        print(result)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    test_bedrock()