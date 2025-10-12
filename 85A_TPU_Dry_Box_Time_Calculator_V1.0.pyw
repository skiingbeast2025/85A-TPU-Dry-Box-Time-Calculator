import json
import os
import sys
from datetime import datetime

# --- History & Setup Files ---
HISTORY_FILE = "history.json"
SETUP_FILE = "setup.json"

# --- Load history ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# --- Save history ---
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# --- Load setup ---
def load_setup():
    if os.path.exists(SETUP_FILE):
        try:
            with open(SETUP_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

# --- Save setup ---
def save_setup(setup):
    with open(SETUP_FILE, "w") as f:
        json.dump(setup, f, indent=4)

# --- Initialize global history and setup ---
history = load_history()
setup = load_setup()

# --- Add history entry ---
def add_history(duration, pre_print, during_print, post_print):
    global history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {
        "timestamp": timestamp,
        "duration": duration,
        "pre_print": pre_print,
        "during_print": during_print,
        "post_print": post_print
    }
    history.append(entry)
    save_history(history)
    if 'update_history_display' in globals():
        update_history_display()

# --- GUI setup ---
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ModuleNotFoundError:
    print("Tkinter not available. GUI disabled.")
    sys.exit(1)

root = tk.Tk()
root.title("85A TPU Drying Calculator")
dark_mode = True

# --- Input: Print Duration ---
root.configure(bg='#1e1e1e')
tk.Label(root, text="Enter print duration:", bg='#1e1e1e', fg='#ffffff').pack(pady=5)
frame_input = tk.Frame(root, bg='#1e1e1e')
frame_input.pack(pady=5)

# Hours and minutes
tk.Label(frame_input, text="Hours:", bg='#1e1e1e', fg='#ffffff').grid(row=0, column=0, padx=2)
entry_hours = tk.Entry(frame_input, width=5, bg='#2e2e2e', fg='#ffffff')
entry_hours.grid(row=0, column=1, padx=2)

tk.Label(frame_input, text="Minutes:", bg='#1e1e1e', fg='#ffffff').grid(row=0, column=2, padx=2)
entry_minutes = tk.Entry(frame_input, width=5, bg='#2e2e2e', fg='#ffffff')
entry_minutes.grid(row=0, column=3, padx=2)

# Days Since Last Print
tk.Label(frame_input, text="Days Since Last Print:", bg='#1e1e1e', fg='#ffffff').grid(row=1, column=0, columnspan=2, pady=5, sticky='w')
entry_days = tk.Entry(frame_input, width=5, bg='#2e2e2e', fg='#ffffff')
entry_days.grid(row=1, column=2, padx=2, columnspan=2, sticky='w')
entry_days.insert(0, str(setup.get("days_since_last", 0)))

# Filament Storage Method
tk.Label(root, text="Filament Storage Method:", bg='#1e1e1e', fg='#ffffff').pack(pady=5)
storage_var = tk.StringVar()
storage_dropdown = ttk.Combobox(root, textvariable=storage_var, state="readonly")
storage_dropdown['values'] = ["Dry Box On", "Dry Box Off", "Sealed Bag", "Open Air"]
storage_dropdown.pack(pady=5)
storage_dropdown.set(setup.get("storage_method", "Dry Box On"))

# Result Label
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, fg='#00bfa6', bg='#1e1e1e').pack(pady=5)

# History
tk.Label(root, text="History:", bg='#1e1e1e', fg='#ffffff').pack(pady=5)
frame_history = tk.Frame(root, bg='#1e1e1e')
frame_history.pack(pady=5, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_list = tk.Listbox(frame_history, width=80, yscrollcommand=scrollbar.set, bg='#2e2e2e', fg='#ffffff')
history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=history_list.yview)

# Button colors
btn_calculate_color = {'bg': '#00bfa6', 'fg': '#ffffff'}
btn_clear_color = {'bg': '#ff5555', 'fg': '#ffffff'}
btn_toggle_color = {'bg': '#ffaa00', 'fg': '#000000'}

# Functions
def calculate():
    try:
        # Get print duration
        hours = int(entry_hours.get() or 0)
        minutes = int(entry_minutes.get() or 0)
        duration = hours * 60 + minutes

        # Get last print info
        days_since_last = int(entry_days.get() or 0)
        storage_method = storage_var.get()

        # Pre-print drying based on storage and last print
        if storage_method == "Dry Box On":
            pre_print = 0 if days_since_last <= 2 else 30
        elif storage_method == "Dry Box Off":
            pre_print = 60 if days_since_last <= 2 else 120
        elif storage_method == "Sealed Bag":
            pre_print = 15 if days_since_last <= 2 else 60
        elif storage_method == "Open Air":
            pre_print = 120
        else:
            pre_print = 0

        # During-print drying
        during_print = duration

        # Post-print drying
        post_print = max(15, round(duration * 0.25))

        # Display results
        result_var.set(f"Pre-Print: {pre_print} min | During-Print: {during_print} min | Post-Print: {post_print} min")

        # Save history
        add_history(duration, pre_print, during_print, post_print)

        # Save setup for next launch
        save_setup({"days_since_last": days_since_last, "storage_method": storage_method})

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for hours, minutes, and days since last print.")

def update_history_display():
    history_list.delete(0, tk.END)
    for i, entry in enumerate(history[::-1], 1):
        text = (f"{i}. [{entry.get('timestamp','N/A')}] Print: {entry.get('duration',0)} min | "
                f"Pre: {entry.get('pre_print',0)} min | During: {entry.get('during_print',0)} min | Post: {entry.get('post_print',0)} min")
        history_list.insert(tk.END, text)

def clear_history():
    global history
    if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
        history = []
        save_history(history)
        update_history_display()

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = '#1e1e1e' if dark_mode else '#ffffff'
    fg_color = '#ffffff' if dark_mode else '#000000'
    entry_bg = '#2e2e2e' if dark_mode else '#ffffff'

    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            if dark_mode:
                widget.configure(bg=btn_calculate_color['bg'], fg=btn_calculate_color['fg'])
            else:
                widget.configure(bg='#00cccc', fg='#000000')
            continue
        try:
            widget.configure(bg=bg_color, fg=fg_color)
        except:
            pass
    for widget in frame_history.winfo_children():
        try:
            widget.configure(bg=entry_bg, fg=fg_color)
        except:
            pass

# Buttons
tk.Button(root, text="Calculate Drying Times", command=calculate, **btn_calculate_color).pack(pady=5)
tk.Button(root, text="Clear History", command=clear_history, **btn_clear_color).pack(pady=5)
tk.Button(root, text="Toggle Dark/Light Mode", command=toggle_mode, **btn_toggle_color).pack(pady=5)

update_history_display()
root.mainloop()
