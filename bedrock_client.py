import boto3
import json
import os
import time

from fallback_analyzer import analyze_protocol_locally

class BedrockClient:
    def __init__(self):
        self._client = None
        self._disabled_until = 0.0
        self.last_error = ""
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'us.anthropic.claude-3-5-haiku-20241022-v1:0')

    @property
    def client(self):
        """Create the AWS client only when AI is actually requested."""
        if self._client is None:
            self._client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
            )
        return self._client

    def _cloud_temporarily_disabled(self) -> bool:
        return time.monotonic() < self._disabled_until

    def _record_cloud_error(self, error: Exception) -> None:
        self.last_error = str(error)
        # Avoid nine identical slow failures during the same 10-user analysis.
        self._disabled_until = time.monotonic() + 300
    
    def chat(self, message: str, system_prompt: str = "") -> str:
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": message}]
                })
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
            
        except Exception as e:
            self._record_cloud_error(e)
            return f"☕ Hello! I'm Random Coffee AI. I'll help you find colleagues for meetings. Error: {str(e)[:50]}..."
    
    def analyze_protocol(self, protocol_text: str, user_data: dict, courses: list) -> dict:
        """Analyze safety protocol and determine course assignments"""
        if self._cloud_temporarily_disabled():
            return analyze_protocol_locally(protocol_text, user_data, courses, self.last_error)

        try:
            # Create course list for AI
            course_list = "\n".join([f"- {c['course_id']}: {c.get('description', 'Safety training course')}" for c in courses])
            
            # Create user context
            user_context = f"User: {user_data['name']} ({user_data['role']}) in {user_data['department']}"
            completed = user_data.get('completed_courses', [])
            if completed:
                user_context += f"\nCompleted courses: {', '.join([c['course_id'] for c in completed])}"
            
            prompt = f"""Analyze this safety protocol and determine if the user needs training courses.

PROTOCOL:
{protocol_text[:1000]}

{user_context}

AVAILABLE COURSES:
{course_list}

Analyze the protocol content and determine:
1. Does this user need any safety training based on the protocol?
2. Which specific courses are relevant?
3. What priority level (critical, high, normal, low)?
4. How often should they renew (months)?
5. Deadline for completion (days)?

Respond in JSON format:
{{
  "should_assign": true/false,
  "recommended_courses": [
    {{
      "course_id": "COURSE_ID",
      "priority": "critical/high/normal/low",
      "renewal_months": 12,
      "deadline_days": 30
    }}
  ],
  "reason": "Brief explanation"
}}"""
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "temperature": 0.3,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            ai_response = result['content'][0]['text']
            
            # Parse JSON response
            try:
                # Extract JSON from response
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = ai_response[json_start:json_end]
                    parsed = json.loads(json_str)
                    if not isinstance(parsed, dict) or not isinstance(parsed.get("recommended_courses", []), list):
                        raise ValueError("Cloud AI response used an unexpected result format")
                    parsed["analysis_source"] = "amazon-bedrock"
                    return parsed
                else:
                    self._record_cloud_error(RuntimeError("Cloud AI response did not contain JSON"))
                    return analyze_protocol_locally(
                        protocol_text, user_data, courses, "Cloud AI response did not contain JSON"
                    )
            except (json.JSONDecodeError, ValueError) as error:
                self._record_cloud_error(error)
                return analyze_protocol_locally(
                    protocol_text, user_data, courses, f"Cloud AI response could not be parsed: {error}"
                )
                
        except Exception as e:
            print(f"Bedrock analysis error: {str(e)}")
            self._record_cloud_error(e)
            return analyze_protocol_locally(protocol_text, user_data, courses, str(e))
