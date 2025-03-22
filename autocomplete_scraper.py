
import requests
import time
import string
import json
import os
import csv
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

# ==== CONFIGURATION ====
API_VERSION = "v1"  # Change to "v2" or "v3" as needed
API_URL = f"http://35.200.185.69:8000/{API_VERSION}/autocomplete?query="
MAX_DEPTH = 5
DELAY = 1.0
MAX_WORKERS = 4

# ==== OUTPUT FILES ====
OUTPUT_PREFIX = f"autocomplete_{API_VERSION}"
CHECKPOINT_FILE = f"{OUTPUT_PREFIX}_checkpoint.json"
OUTPUT_FILE = f"{OUTPUT_PREFIX}_names.txt"
JSON_FILE = f"{OUTPUT_PREFIX}_names.json"
CSV_FILE = f"{OUTPUT_PREFIX}_names.csv"
SUMMARY_FILE = f"{OUTPUT_PREFIX}_summary.txt"

# ==== GLOBAL STATE ====
visited = set()
results = set()
lock = Lock()
request_count = 0

# ==== CHECKPOINTING ====
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

# ==== FETCHING FUNCTION ====
def fetch_names(query):
    global request_count
    try:
        response = requests.get(API_URL + query)
        with lock:
            request_count += 1
        if response.status_code == 200:
            return response.json().get("names", [])
        print(f"[!] Error {response.status_code} for query: '{query}'")
    except Exception as e:
        print(f"[!] Exception for '{query}': {e}")
    return []

# ==== RECURSIVE EXPLORATION ====
def explore(query, depth=0):
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

# ==== MULTITHREADING WRAPPER ====
def threaded_explore():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(explore, c) for c in string.ascii_lowercase]
        for future in futures:
            future.result()

# ==== MAIN FUNCTION ====
def main():
    global visited, results
    print(f"[*] Starting scraper for API version: {API_VERSION}")
    visited, results = load_checkpoint()
    print(f"[*] Loaded checkpoint with {len(visited)} visited and {len(results)} results.")

    start = time.time()
    threaded_explore()
    end = time.time()

    # Save results as TXT
    with open(OUTPUT_FILE, "w") as f:
        for name in sorted(results):
            f.write(name + "\n")
    print(f"✅ Results saved to {OUTPUT_FILE}")

    # Save results as JSON
    with open(JSON_FILE, "w") as f_json:
        json.dump(sorted(results), f_json, indent=2)
    print(f"✅ Results saved to {JSON_FILE}")

    # Save results as CSV
    with open(CSV_FILE, "w", newline="") as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["name"])
        for name in sorted(results):
            writer.writerow([name])
    print(f"✅ Results saved to {CSV_FILE}")

    # Save summary
    with open(SUMMARY_FILE, "w") as summary:
        summary.write(f"Total API requests made: {request_count}\n")
        summary.write(f"Total unique names found: {len(results)}\n")
        summary.write(f"Prefixes visited: {len(visited)}\n")
    print(f"📝 Summary saved to {SUMMARY_FILE}")
    print(f"📨 Total requests: {request_count}, Names found: {len(results)}, Time: {end - start:.2f}s")

if __name__ == "__main__":
  
    main()
with open(OUTPUT_FILE, "w") as f:
    for name in sorted(results):
        f.write(name + "\n")
print(f"✅ Results saved to {OUTPUT_FILE}")
