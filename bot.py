import random
import re
import requests
from config import USER_AGENT, REQUEST_TIMEOUT
from storage import load_memory, save_memory

responses = {
    "hello": ["Hi there!", "Hello!", "Hey, how can I help you?"],
    "how are you": ["I'm doing great, thanks!", "All systems running smoothly!", "I'm fine, how about you?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "tell me a joke": ["Why did the computer go to the doctor? Because it caught a virus!"],
    "default": ["Sorry, I didn’t understand that.", "Can you rephrase?", "Hmm, I’m not sure about that."]
}

memory = load_memory()

def search_wikipedia(query):
    formatted = query.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json().get("extract", "No summary found.")
        if r.status_code == 404:
            return "I couldn’t find a page for that topic."
        return f"Couldn’t fetch info right now (status {r.status_code})."
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException:
        return "Network error. Check your internet and try again."

def get_response(user_input):
    user_input = user_input.lower()

    if user_input.startswith("search ") or user_input.startswith("tell me about "):
        topic = user_input.replace("search ", "").replace("tell me about ", "")
        return search_wikipedia(topic)

    match = re.match(r"my name is (.*)", user_input)
    if match:
        name = match.group(1).capitalize()
        memory["name"] = name
        save_memory(memory)
        return f"Nice to meet you, {name}!"

    match = re.match(r"remember that i like (.*)", user_input)
    if match:
        hobby = match.group(1)
        memory["hobby"] = hobby
        save_memory(memory)
        return f"Got it! I’ll remember that you like {hobby}."

    if "what do you remember" in user_input:
        return f"I remember: {memory}" if memory else "I don’t remember anything yet."

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return random.choice(responses["default"])
