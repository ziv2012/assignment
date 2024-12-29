import json
import uvicorn
import asyncio
from fastapi import FastAPI
from openai import OpenAI

from app.routers.api import router
from app.services.openai_service import openai_service

app = FastAPI(title="GenAI Detection Service")

app.include_router(router)

async def run():
    result = await openai_service.classify_prompt("I need a loan", {"healthcare": True, "finance": False, "legal": True, "hr": False})
    print(result)
    result2 = await openai_service.classify_prompt_fast("I need a loan", {"healthcare": True, "finance": False, "legal": True, "hr": False})
    print(result2)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # asyncio.run(run())