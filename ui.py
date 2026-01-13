import tkinter as tk
import datetime
from bot import get_response
from config import APP_TITLE, WINDOW_SIZE, COLOR_USER, COLOR_BOT, COLOR_META

def run_ui():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(WINDOW_SIZE)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_log = tk.Text(frame, bg="white", fg="black", wrap=tk.WORD, yscrollcommand=scrollbar.set)
    chat_log.config(state=tk.DISABLED)
    chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=chat_log.yview)

    chat_log.tag_config("user", foreground=COLOR_USER)
    chat_log.tag_config("bot", foreground=COLOR_BOT)
    chat_log.tag_config("meta", foreground=COLOR_META)

    def append_message(sender, text):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        chat_log.config(state=tk.NORMAL)
        tag = "user" if sender == "You" else "bot"
        chat_log.insert(tk.END, f"{sender}: ", tag)
        chat_log.insert(tk.END, f"{text}\n")
        chat_log.insert(tk.END, f"{timestamp}\n\n", "meta")
        chat_log.see(tk.END)
        chat_log.config(state=tk.DISABLED)

    entry_box = tk.Entry(root, width=40)
    entry_box.pack(side=tk.LEFT, padx=10, pady=10)

    def send_message(event=None):
        user_input = entry_box.get().strip()
        if not user_input:
            return
        entry_box.delete(0, tk.END)
        append_message("You", user_input)
        try:
            response = get_response(user_input)
        except Exception:
            response = "Something went wrong. Please try again."
        append_message("Chatbot", response)

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    clear_button = tk.Button(root, text="Clear", command=lambda: chat_log.delete("1.0", tk.END))
    clear_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.bind('<Return>', send_message)
    entry_box.focus_set()
    root.mainloop()
