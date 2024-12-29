from datetime import datetime
from typing import Dict, List
from app.models.schemas import LogEntry

class AuditLogger:
    def __init__(self):
        self.logs = []

    def log_request(self, endpoint: str, prompt: str, settings: Dict[str, bool], 
                   result: List[str], processing_time: float):
        """Log the request detils"""
        log_entry = LogEntry(
            timestamp=datetime.now(),
            endpoint=endpoint,
            prompt=prompt,
            settings=settings,
            result=result,
            processing_time=processing_time
        )
        self.logs.append(log_entry)

    def get_recent_logs(self, limit: int = 100):
        """Return the most recnet logs, limited by the specified number"""
        return sorted(self.logs, key=lambda x: x.timestamp, reverse=True)[:limit]

# Create a single instance to be used across the application
audit_logger = AuditLogger()