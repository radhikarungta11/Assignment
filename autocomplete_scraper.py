
import requests
import time
import string
import json
import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://35.200.185.69:8000/v1/autocomplete?query="
DELAY = 1.0  # delay between requests in seconds
MAX_DEPTH = 5
MAX_WORKERS = 4  # max parallel workers
CHECKPOINT_FILE = "checkpoint.json"
OUTPUT_FILE = "all_names.txt"

# Thread-safe containers
visited = set()
results = set()
lock = Lock()

# Load checkpoint if it exists
def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("visited", [])), set(data.get("results", []))
    return set(), set()

def save_checkpoint():
    with lock:
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump({
                "visited": list(visited),
                "results": list(results)
            }, f)

def fetch_names(query):
    """Fetch names for a given query prefix."""
    try:
        response = requests.get(API_URL + query)
        if response.status_code == 200:
            return response.json().get("names", [])
        print(f"[!] Error {response.status_code} for query: '{query}'")
    except Exception as e:
        print(f"[!] Exception for '{query}': {e}")
    return []

def explore(query, depth=0):
    """Recursively explore query prefixes."""
    with lock:
        if query in visited or depth > MAX_DEPTH:
            return
        visited.add(query)

    time.sleep(DELAY)
    names = fetch_names(query)

    with lock:
        for name in names:
            results.add(name)
        save_checkpoint()

    if names:
        for c in string.ascii_lowercase:
            explore(query + c, depth + 1)

def threaded_explore():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(explore, c) for c in string.ascii_lowercase]
        for future in futures:
            future.result()  # wait for all to complete

def main():
    global visited, results
    print("[*] Loading checkpoint if available...")
    visited, results = load_checkpoint()

    print(f"[*] Starting crawl with {len(visited)} prefixes already visited.")
    start = time.time()
    threaded_explore()
    end = time.time()

    print(f"\n✅ Completed in {end - start:.2f}s. Total unique names: {len(results)}")
    with open(OUTPUT_FILE, "w") as f:
        for name in sorted(results):
            f.write(name + "\n")
    print(f"✅ Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
with open(OUTPUT_FILE, "w") as f:
    for name in sorted(results):
        f.write(name + "\n")
print(f"✅ Results saved to {OUTPUT_FILE}")
