# 🧮 Project: TPU Drying Time Calculator
# Description:
# This is a simple Python GUI app built using Tkinter.
# The goal is to calculate recommended drying times for A85 TPU filament
# based on the duration of a 3D print.
#
# 💡 Functionality:
# - User enters the print duration (hours and minutes)
# - The app calculates:
#     • Pre-drying time (proportional to print duration)
#     • Post-drying time (about half of the pre-drying time)
# - All drying assumes 50°C drying temperature
# - Results are displayed clearly in a small GUI window
#
# 🧰 Tech:
# - Language: Python 3.x
# - App icon set via root.iconbitmap
#   (requires .ico file at specified path)
#   Example: root.iconbitmap(r"C:\Users\Aidri\Downloads\Untitled design.ico")
# - Library: Tkinter for GUIroot:#
# 🎯 Goals for Cursor AI:
# - Maintain clean, readable code
# - Keep GUI minimal and user-friendly
# - Optionally allow later customization (themes, extra features)

import tkinter as tk
from tkinter import ttk
from math import floor

def calculate_dry_time():
    try:
        hours = float(entry_hours.get() or 0)
        minutes = float(entry_minutes.get() or 0)
        total_print_time = hours + minutes / 60

        if total_print_time <= 0:
            result_pre.set("Please enter a valid time.")
            result_post.set("")
            return

        # Drying logic (proportional model)
        pre_dry_hours = 2 + (total_print_time * 0.7)  # base + proportional factor
        post_dry_hours = pre_dry_hours * 0.5

        def format_time(hours):
            h = floor(hours)
            m = round((hours - h) * 60)
            return f"{h} hr {m} min" if h or m else "0 min"

        pre_text = format_time(pre_dry_hours)
        post_text = format_time(post_dry_hours)

        result_pre.set(f"Pre-Dry: {pre_text}")
        result_post.set(f"Post-Dry: {post_text}")

        # Add entry to history
        history_text.config(state='normal')
        history_text.insert(tk.END, f"Print: {hours} hr {minutes} min → Pre-Dry: {pre_text} | Post-Dry: {post_text}\n")
        history_text.see(tk.END)
        history_text.config(state='disabled')

    except ValueError:
        result_pre.set("Invalid input.")
        result_post.set("")

# --- UI Setup ---
root = tk.Tk()
root.title("A85 TPU Drying Time Calculator")
root.geometry("480x500")
root.configure(bg="#1e1e1e")

# Set app icon
try:
    root.iconbitmap(r"C:\Users\Aidri\Downloads\3d-printer-icon.ico")
except:
    # Fallback if icon file is not found
    pass

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#00bfa6", foreground="white")
style.map("TButton", background=[("active", "#00a894")])

# --- Input fields ---
ttk.Label(root, text="Print Duration").pack(pady=(20, 5))
frame_input = tk.Frame(root, bg="#1e1e1e")
frame_input.pack()
tk.Label(frame_input, text="Hours:", bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=5)
entry_hours = ttk.Entry(frame_input, width=6)
entry_hours.grid(row=0, column=1, padx=5)
tk.Label(frame_input, text="Minutes:", bg="#1e1e1e", fg="white").grid(row=0, column=2, padx=5)
entry_minutes = ttk.Entry(frame_input, width=6)
entry_minutes.grid(row=0, column=3, padx=5)

ttk.Button(root, text="Calculate", command=calculate_dry_time).pack(pady=15)

# --- Results ---
result_pre = tk.StringVar()
result_post = tk.StringVar()
ttk.Label(root, textvariable=result_pre, font=("Segoe UI", 11, "bold")).pack(pady=3)
ttk.Label(root, textvariable=result_post, font=("Segoe UI", 11, "bold")).pack(pady=3)

# --- Tips section ---
tips_text = (
    "💡 Tips:\n"
    "• Keep dryer at 50 °C for TPU.\n"
    "• Post-dry ≈ half of pre-dry time.\n"
    "• Store filament in sealed bag or dryer.\n"
    "• Watch for stringing or popping as signs of moisture."
)
tk.Label(root, text=tips_text, bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 9), justify="left", wraplength=440).pack(pady=10)

# --- History section ---
history_frame = tk.Frame(root, bg="#1e1e1e")
history_frame.pack(fill='both', expand=True, padx=10, pady=5)

history_scroll = tk.Scrollbar(history_frame)
history_scroll.pack(side='right', fill='y')

history_text = tk.Text(history_frame, height=10, bg="#2e2e2e", fg="white", font=("Segoe UI", 10), yscrollcommand=history_scroll.set)
history_text.pack(side='left', fill='both', expand=True)
history_text.config(state='disabled')  # read-only

history_scroll.config(command=history_text.yview)

root.mainloop()
