# Assignment


# 🧠 Autocomplete Name Scraper

This project is a Python-based scraper to extract **all possible names** from an undocumented autocomplete API running at:http://35.200.185.69:8000/v1/autocomplete?query=<string>


The API has no official documentation, so this project reverse-engineers the endpoint and recursively explores name prefixes to discover the full dataset of available names.

---

## 🚀 Features

- ✅ Recursive name discovery by prefix
- ✅ Rate limit-aware with throttling
- ✅ Checkpointing for resuming interrupted runs
- ✅ Multithreaded for faster crawling
- ✅ Saves results to `.txt`, `.json`, and `.csv`

---

## 📦 Files

- `autocomplete_scraper.py` – The main scraper script
- `all_names.txt` – All discovered names (one per line)
- `all_names.json` – Names saved as a JSON array
- `all_names.csv` – Names in CSV format
- `checkpoint.json` – Stores progress for resuming
- `README.md` – This file

---

## 🧠 Approach

### 1. Endpoint Testing
We discovered the API responds to:/v1/autocomplete?query=<string>

Passing single or multiple characters returns a list of suggested names.

### 2. Recursive Brute Force
- Start with each letter `a-z`.
- Request names using the current prefix.
- If names are returned, recursively go deeper by adding a-z to the prefix.
- Stop exploring deeper if no names are returned for a prefix.

### 3. Optimization
- Added a **checkpoint system** to resume progress after interruptions.
- Used a **thread pool** to parallelize crawling across multiple prefixes.
- **Throttled requests** to avoid triggering API rate limits.

---

## 📈 Results

The number of unique names discovered depends on:
- The `MAX_DEPTH` of prefix exploration.
- The API’s autocomplete logic (whether it shows all available matches).

Check `all_names.txt` or `all_names.csv` for the full output.

---

## 🛠 Usage

### ▶️ Run the scraper

```bash
python autocomplete_scraper.py




 1. Basic Request Test
    Try simple queries like a, b, c, etc., using http://35.200.185.69:8000/v1/autocomplete?query=a.
    Observe the response format (likely JSON).
    
2.Response Analysis
Check for key properties: name, suggestions, etc.
See if results change with longer prefixes (ab, abc, etc.).

3. Alphabet Brute Force
 Generate all prefixes recursively from a to z (and possibly 0–9).
For each prefix, get the autocomplete response.
Add new results to a set (to ensure uniqueness).
Recurse only if new names keep appearing with deeper prefixes.

4. Handle Rate Limits
Look at response headers or status codes.
Implement retry logic and throttling (e.g., 1 request per second).

5.Edge Cases
Empty query? Query with special characters? Upper vs lower case?

6.Stopping Criteria
If no new results are returned from deeper queries.



MORE FEATURES

Logging- Console logs for errors and progress.
Checkpointing-Saves visited prefixes and results to disk in checkpoint.json.
Parallel Requests-Uses up to MAX_WORKERS threads to explore in parallel.
Safe Throttling-Keeps DELAY between each request to reduce risk of rate limiting.


