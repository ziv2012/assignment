import time
from openai import AsyncOpenAI
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url='https://api.aim.security/managed-ai/v1/ai-proxy/openai'
        )

    async def classify_prompt(self, prompt: str, active_topics: Dict[str, bool]) -> List[str]:
        """
        Use OpenAI's API to classify the prompt into topics.
        """
        enabled_topics = [topic for topic, enabled in active_topics.items() if enabled]
        if not enabled_topics:
            return []
        


        system_prompt = f"""
            You are a specialized content classifier. Analyze the given text and identify any topics clearly present from the following list: {', '.join(enabled_topics)}. 
            Each topic corresponds to specific subject areas, so only detect a topic if the text provides clear, explicit cues for it. If no topics are detected, return an empty JSON object.

            Output your response strictly as a JSON object with a key "detected_topics", following this format:
            {{"detected_topics": ["health", "finance"]}}
            If no topics are detected, return:
            {{"detected_topics": []}}

            Guidelines:
            1. Focus only on topics enabled in the provided settings.
            2. Ensure that detected topics directly relate to the content.
            3. If multiple topics are relevant, include all applicable topics.
            4. If no topics match, return:
            {{"detected_topics": []}}
            5. Do not include explanations, additional text, or empty strings in the response.
            """

        print(f"System prompt: {system_prompt}")
        print(f"User prompt: {prompt}")
        # Time check 
        start_time = time.time()
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={ "type": "json_object" }
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"Result: {result}")
            print(f"Time taken: {time.time() - start_time}")
            return result.get("detected_topics", [])
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return []

    async def classify_prompt_fast(self, prompt: str, active_topics: Dict[str, bool]) -> List[str]:
        """
        Faster version that returns after finding the first topic.
        Uses a more focused system prompt to encourage faster response.
        """
        enabled_topics = [topic for topic, enabled in active_topics.items() if enabled]
        if not enabled_topics:
            return []

        system_prompt = f"""
            You are a rapid-response content classifier. Analyze the given text and quickly determine if it contains any of these topics: {', '.join(enabled_topics)}. 
            Focus on identifying the first relevant topic and return immediately upon finding a match. Ensure the detected topic is accurate before stopping further analysis.

            Output your response strictly as a JSON object in the following format:
            {{"detected_topics": ["health", "finance"]}}
            If no match is found after a brief scan, return:
            {{"detected_topics": []}}

            Guidelines:
            1. Evaluate the text in order and stop as soon as you identify the first enabled topic.
            2. Consider only the topics listed in the provided settings.
            3. Ensure that the detected topic is clearly relevant and present in the text.
            4. If no match is found quickly, return:
            {{"detected_topics": []}}
            5. Do not include explanations, additional text, or empty strings in the response.
            """
        # Time check
        start_time = time.time()
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={ "type": "json_object" }
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"Time taken: {time.time() - start_time}")
            return result.get("detected_topics", [])[:1]  # Only return the first topic
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return []

# Create a single instance to be used across the application
openai_service = OpenAIService()