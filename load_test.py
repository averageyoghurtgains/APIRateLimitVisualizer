import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000/heavy-task"

def send_request(i):
    try:
        response = requests.get(BASE_URL)
        print(f"Request {i} finished: {response.status_code}")
    except Exception as e:
        print(f"Request {i} failed: {e}")

def run_steady_load(total=20):
    """Sends requests one after another (Sequential)"""
    print(f"\n--- Starting Steady Load ({total} requests) ---")
    for i in range(total):
        send_request(i)
        time.sleep(0.2)  # Short pause between requests

def run_burst_load(total=600):
    """Sends many requests at the exact same time (Parallel/Spark-style)"""
    print(f"\n--- Starting Burst Load ({total} requests) ---")
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(send_request, range(total))

if __name__ == "__main__":
    # 1. First, show some steady traffic
    run_steady_load(30)
    
    print("\nWaiting 3 seconds before the big spike...")
    time.sleep(3)
    
    # 2. Then, hit it with a massive burst to see the chart spike
    run_burst_load(600)