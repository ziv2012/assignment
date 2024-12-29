from typing import Dict, List
from app.services.openai_service import openai_service

class TopicDetector:
    @staticmethod
    async def detect_topics(text: str, active_topics: Dict[str, bool], fast_mode: bool = False) -> List[str]:
        """
        Analyze text for specified topics using OpenAI's API.
        If fast_mode is True, return after finding the first match.
        """
        if fast_mode:
            return await openai_service.classify_prompt_fast(text, active_topics)
        else:
            return await openai_service.classify_prompt(text, active_topics)