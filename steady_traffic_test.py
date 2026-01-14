import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Settings
BASE_URL = "http://localhost:8000/heavy-task"
TARGET_RPS = 4 

def send_request():
    try:
        requests.get(BASE_URL, timeout=1)
    except Exception:
        pass # Ignore errors to keep the loop moving

def run_steady_worker():
    print(f"Starting steady load at {TARGET_RPS} RPS")
    print("Press Ctrl+C to stop.")
    
    while True:
        start_time = time.time()
        
        # Fire the request
        send_request()
        
        # Calculate how long to sleep to maintain the rate
        # If we want 5 RPS, each request should take 0.2 seconds total
        wait_time = 1.0 / TARGET_RPS
        elapsed = time.time() - start_time
        
        sleep_duration = max(0, wait_time - elapsed)
        time.sleep(sleep_duration)

if __name__ == "__main__":
    run_steady_worker()