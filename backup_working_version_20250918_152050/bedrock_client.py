import os, json, boto3
from botocore.config import Config

class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            config=Config(retries={"max_attempts": 3, "mode": "standard"})
        )
        self.model_id = os.getenv("BEDROCK_MODEL_ID")

    def analyze_protocol(self, protocol_text: str, user_data: dict, course_data: list) -> dict:
        # Короткий промпт для быстрой обработки
        prompt = f"""
Протокол: {protocol_text[:300]}...
Пользователь: {user_data['role']} в {user_data['department']}

Нужны ли курсы, какой приоритет, периодичность и дедлайн?
Ответь JSON: {{"should_assign": true, "recommended_courses": [{{"course_id": "HAZCOM-1910.1200", "priority": "critical", "renewal_months": 12, "deadline_days": 7}}], "reason": "кратко"}}
Приоритеты: critical=критичный, high=высокий, normal=обычный, low=низкий
Периоды: 6=полгода, 12=год, 24=2года
Дедлайны: 3=3дня, 7=неделя, 14=2недели, 30=месяц
"""
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        }
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )
        
        result = json.loads(response["body"].read())
        ai_response = result["content"][0]["text"]
        
        # Извлекаем JSON из ответа AI
        try:
            start = ai_response.find('{')
            end = ai_response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = ai_response[start:end]
                result = json.loads(json_str)
                
                # Преобразуем старый формат в новый
                if "recommended_courses" in result and result["recommended_courses"]:
                    if isinstance(result["recommended_courses"][0], str):
                        old_courses = result["recommended_courses"]
                        result["recommended_courses"] = []
                        for course_id in old_courses:
                            result["recommended_courses"].append({
                                "course_id": course_id,
                                "priority": "normal",
                                "renewal_months": 12,
                                "deadline_days": 30
                            })
                
                return result
        except:
            pass
        
        # Если не удалось распарсить, возвращаем базовый ответ
        return {
            "should_assign": True,
            "recommended_courses": [
                {"course_id": "HAZCOM-1910.1200", "renewal_months": 12},
                {"course_id": "LAB-SAFETY-101", "renewal_months": 12}
            ],
            "reason": "Протокол касается работы с химическими веществами"
        }