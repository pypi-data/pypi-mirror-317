# autohint/suggestion.py

import threading
import time
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import requests
from functools import lru_cache

# Thread-safe global variable for storing suggestions
suggestions = []
lock = threading.Lock()

# Debounce mechanism
last_query_time = 0
debounce_interval = 0.3  # Seconds

# Cache to store recent queries and their results
@lru_cache(maxsize=100)
def fetch_suggestions_cached(query):
    """
    Fetch suggestions from the internet for a given query.
    This function is cached to prevent redundant API calls.
    """
    url = f"https://api.datamuse.com/sug?s={query}"  # Example API
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        return [item['word'] for item in response.json()]
    except requests.RequestException:
        return []

def fetch_suggestions(query):
    """
    Fetch suggestions and update the global variable safely.
    Implements debouncing to reduce excessive API calls.
    """
    global suggestions, last_query_time
    current_time = time.time()
    if current_time - last_query_time < debounce_interval:
        return  # Skip fetching if debounce interval not elapsed
    last_query_time = current_time

    results = fetch_suggestions_cached(query)
    with lock:
        suggestions.clear()
        suggestions.extend(results)

class InternetSuggestionCompleter(Completer):
    def get_completions(self, document, complete_event):
        global suggestions
        word = document.text.strip()

        # Start a new thread to fetch suggestions if input changes
        if word:
            thread = threading.Thread(target=fetch_suggestions, args=(word,))
            thread.daemon = True  # Ensure thread stops with the main program
            thread.start()

        # Display available suggestions
        with lock:
            for suggestion in suggestions:
                if word.lower() in suggestion.lower():
                    yield Completion(suggestion, start_position=-len(word))

def search_bar():
    """
    Interactive search bar with real-time suggestions.
    This version doesn't store or print the selected input.
    """
    print("Start typing to get real-time suggestions (press Enter to select):")
    prompt("> ", completer=InternetSuggestionCompleter())  # Only suggest, no result printed