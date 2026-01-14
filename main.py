import time
from collections import deque
from fastapi import FastAPI, Request
import asyncio

app = FastAPI()

class MetricsManager:
    def __init__(self):
        self.request_timestamps = deque() 
        self.total_requests = 0

    def record_request(self):
        self.total_requests += 1
        self.request_timestamps.append(time.time())

    def get_kpis(self):
        now = time.time()
        # Only look at the last 1.0 second for a "real-time" feel
        recent_reqs = [t for t in self.request_timestamps if t > (now - 1.0)]
        
        # Keep the deque clean (remove anything older than 5 seconds)
        while self.request_timestamps and self.request_timestamps[0] < (now - 5):
            self.request_timestamps.popleft()
            
        return {
            "total_requests": self.total_requests,
            "current_rps": len(recent_reqs)
        }

metrics = MetricsManager()

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    if request.url.path != "/stats":
        metrics.record_request()
    return await call_next(request)

@app.get("/stats")
async def get_stats():
    return metrics.get_kpis()

@app.get("/heavy-task")
async def heavy():
    await asyncio.sleep(0.1) 
    return {"status": "done"}