
import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import ttk

# --- -State 
clicking = False
click_interval = 0.1
current_hotkey = "F6"

# -------------------- Auto Clicker Logic 
def auto_clicker():
    global clicking
    while True:
        if clicking:
            pyautogui.click()
            time.sleep(click_interval)
        else:
            time.sleep(0.05)

def toggle_clicking():
    global clicking
    clicking = not clicking
    update_status()

def update_status():
    status_label.config(
        text=f"Status: {'RUNNING' if clicking else 'STOPPED'}",
        foreground="green" if clicking else "red"
    )

# -------------------- GUI Actions --------------------
def update_interval(val):
    global click_interval
    click_interval = float(val)

def set_hotkey():
    global current_hotkey
    new_key = hotkey_entry.get().strip()

    if not new_key:
        return

    keyboard.remove_hotkey(current_hotkey)
    keyboard.add_hotkey(new_key, toggle_clicking)

    current_hotkey = new_key
    hotkey_status.config(text=f"Hotkey: {current_hotkey}")

def on_close():
    keyboard.unhook_all()
    root.destroy()

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Python Auto Clicker")
root.geometry("320x260")
root.resizable(False, False)

ttk.Label(root, text="Auto Clicker", font=("Arial", 15, "bold")).pack(pady=8)

status_label = ttk.Label(root, text="Status: STOPPED", foreground="red")
status_label.pack(pady=5)

ttk.Label(root, text="Click Interval (seconds)").pack()
interval_slider = ttk.Scale(
    root, from_=0.01, to=1.0, value=0.1, command=update_interval
)
interval_slider.pack(fill="x", padx=25)

ttk.Label(root, text="Start / Stop Hotkey").pack(pady=(12, 0))
hotkey_entry = ttk.Entry(root, justify="center")
hotkey_entry.insert(0, current_hotkey)
hotkey_entry.pack()

ttk.Button(root, text="Set Hotkey", command=set_hotkey).pack(pady=6)

hotkey_status = ttk.Label(root, text=f"Hotkey: {current_hotkey}")
hotkey_status.pack()

ttk.Label(root, text="Press the hotkey to toggle clicking\nClose window to exit").pack(pady=10)

# -------------------- Background Thread --------------------
thread = threading.Thread(target=auto_clicker, daemon=True)
thread.start()

keyboard.add_hotkey(current_hotkey, toggle_clicking)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
