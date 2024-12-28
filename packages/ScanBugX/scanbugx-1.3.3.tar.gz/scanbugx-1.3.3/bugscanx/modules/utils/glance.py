import os
import json
import requests
import threading
from rich.text import Text
from rich.style import Style
from rich.console import Console
from datetime import datetime, timedelta

console = Console()

LOCAL_MESSAGE_FILE = ".message.json"

def fetch_and_store_message():
    url = "https://raw.githubusercontent.com/for-testing-something/test1/refs/heads/main/message.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(LOCAL_MESSAGE_FILE, "w", encoding="utf-8") as file:
                file.write(response.text.encode('utf-8').decode('utf-8'))
            return True, None
    except Exception:
        pass
    return False, None

def load_local_message():
    if not os.path.exists(LOCAL_MESSAGE_FILE):
        return None, None
    try:
        with open(LOCAL_MESSAGE_FILE, "r", encoding="utf-8") as file:  # Added encoding="utf-8"
            data = json.load(file)
            message = " " + data.get("message", "").strip()  # Added a space before the message
            styles = data.get("styles", [])
            if message:
                styled_message = Text()
                last_index = 0
                for style in styles:
                    text = style.get("text", "")
                    color = style.get("color", "white")
                    if text in message:
                        start_index = message.find(text, last_index)
                        end_index = start_index + len(text)
                        if start_index > last_index:
                            styled_message.append(message[last_index:start_index])
                        styled_message.append(text, style=Style(color=color))
                        last_index = end_index
                if last_index < len(message):
                    styled_message.append(message[last_index:])
                return styled_message, None
    except Exception:
        pass
    return None, None

def get_greeting_message():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return " Good morning! Hope your day’s off to a great start!"
    elif 12 <= current_hour < 18:
        return " Good afternoon! Hope you're having a fantastic day!"
    else:
        return " Good evening! Hope your day was productive!"

def is_local_message_outdated():
    if not os.path.exists(LOCAL_MESSAGE_FILE):
        return True
    try:
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(LOCAL_MESSAGE_FILE))
        return datetime.now() - file_mod_time > timedelta(hours=3)
    except Exception:
        pass
    return True

def display_message():
    try:
        message, _ = load_local_message()
        if message:
            console.print(message, style="bold")
        else:
            console.print(get_greeting_message(), style="bold cyan")

        def fetch_and_update():
            try:
                if is_local_message_outdated():
                    fetch_and_store_message()
            except Exception:
                pass
        thread = threading.Thread(target=fetch_and_update)
        thread.daemon = True
        thread.start()
    except Exception:
        pass
