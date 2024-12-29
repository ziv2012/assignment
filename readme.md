# GenAI Detection Service

A FastAPI-based service designed to analyze and detect specific topics in text prompts using OpenAI's GPT models. This service provides real-time content analysis with configurable topic detection.

## Features

- Topic detection in text prompts
- Configurable topic settings
- Fast-mode detection for time-critical operations
- Request logging and auditing
- Asynchronous processing for better performance

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd detection-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
detection_service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── openai_service.py
│   └── routers/
│       ├── __init__.py
│       └── api.py
└── requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. The service exposes the following endpoints:

### /detect
Analyzes text for all configured topics.

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "How would you suggest to treat depression?",
    "settings": {
        "health": true,
        "finance": false,
        "hr": true,
        "legal": false
    }
  }'
```

### /protect
Fast analysis that returns after finding the first matching topic.

```bash
curl -X POST "http://localhost:8000/protect" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the legal implications of employee benefits?",
    "settings": {
        "health": true,
        "finance": true,
        "hr": true,
        "legal": true
    }
  }'
```

### /logs
Retrieve audit logs of previous requests.

```bash
curl "http://localhost:8000/logs?limit=10"
```

## API Response Format

The API returns responses in the following format:

```json
{
    "detected_topics": ["health"]
}
```

## Development

- The service uses FastAPI's automatic API documentation
- Access the API documentation at `http://localhost:8000/docs`
- Access the alternative API documentation at `http://localhost:8000/redoc`

## Performance Considerations

- The service uses asynchronous processing for better performance
- OpenAI API calls are made asynchronously to prevent blocking

## Decisions I Had to Make (Tradeoffs):

- While working on this project, I had to make some calls. 
  One of the big ones is simple rate limiting
  I'm currently relying on OpenAI's rate limits without implementing 
  my own rate limiting layer. 
  This makes the code simpler but could lead to unnecessary API calls and costs if I get heavy traffic.

- In-memory logging. 
  I know it’s not ideal since everything gets wiped if the service restarts, 
  but I wanted to make sure the core functionality was up and running first.

- Another decision was keeping error handling pretty basic. 
  It wasn’t easy to settle for that since I know how critical proper error handling is, 
  but I figured it’s something I could refine later. 
  For now, focusing on the main features helped me move faster.

## What’s Next (Next Steps):
- If I were to continue developing this, the first thing I’d focus on is improving the error handling. 
  It’s definitely the weakest link right now, and adding clear error types and meaningful messages for clients would make a big difference.

- Another priority would be adding real observability. 
  Right now, there’s no way to monitor the service’s performance in real-time or troubleshoot effectively when things go wrong.

- Performance also needs attention. Adding caching if possiable would be a game changer, and implementing rate limiting is essential before this is ready for production use.

- Testing is a big area I’d want to tackle too. 
  Proper unit tests and load testing are crucial to ensure the service can handle pressure.

- Lastly, documentation needs an upgrade. Nothing fancy—just straightforward instructions on how to set everything up and use the API effectively.