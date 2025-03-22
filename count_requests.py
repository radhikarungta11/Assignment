import json
import os

CHECKPOINT_FILE = "checkpoint.json"

def count_requests(checkpoint_path):
    if not os.path.exists(checkpoint_path):
        print("❌ checkpoint.json not found.")
        return

    with open(checkpoint_path, "r") as f:
        data = json.load(f)
        visited = data.get("visited", [])
        print(f"📨 Total API requests made: {len(visited)}")
        print(f"🔍 Example queried prefixes: {visited[:10]}")

if __name__ == "__main__":
    count_requests(CHECKPOINT_FILE)
