import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import classalg  # Ensure this is in the same directory

# --- Setup Main Window ---
root = tk.Tk()
root.title("Class CSV Processor")
root.geometry("1000x600")
root.resizable(False, False)

dark_mode_enabled = False

# --- Toggle Dark Mode ---
def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled

    if dark_mode_enabled:
        colors = {
            "bg": "#2E2E2E", "fg": "#FFFFFF", "button_bg": "#444", "button_fg": "#FFF",
            "entry_bg": "#1E1E1E", "tree_bg": "#1E1E1E", "tree_fg": "#FFFFFF", "highlight": "#101445"
            
        }
    else:
        colors = {
            "bg": "#F0F0F0", "fg": "#000000", "button_bg": "#FFF", "button_fg": "#000",
            "entry_bg": "#FFFFFF", "tree_bg": "#FFFFFF", "tree_fg": "#000000", "highlight": "#7777FF"
            
        }

    root.config(bg=colors["bg"])
    frame_top.config(bg=colors["bg"])
    selected_file_label.config(bg=colors["bg"], fg=colors["fg"])
    status_label.config(bg=colors["bg"], fg=colors["fg"])
    open_button.config(bg=colors["button_bg"], fg=colors["button_fg"])
    process_button.config(bg=colors["button_bg"], fg=colors["button_fg"])
    dark_mode_button.config(bg=colors["button_bg"], fg=colors["button_fg"])
    for child in tree.get_children():
        tree.item(child, tags=("row",))
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", background=colors["tree_bg"], foreground=colors["tree_fg"], fieldbackground=colors["tree_bg"])
    style.map("Treeview", background=[("selected", colors["highlight"])])
    style.configure("Treeview.Heading", background=colors["bg"], foreground=colors["fg"])
    style.map("Treeview.Heading", background=[("active", colors["highlight"])])
    style.configure("TScrollbar", background=colors["bg"], troughcolor=colors["bg"])

# --- Load CSV ---
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select your class file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        selected_file_label.config(text=f"Selected File:\n{os.path.basename(file_path)}")
        try:
            process_file(file_path)
            status_label.config(text="✅ File processed.", fg="green")
        except Exception as e:
            status_label.config(text=f"❌ Error: {str(e)}", fg="red")

def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    if not lines:
        raise Exception("Empty file.")
    data = [line.split(",", 1)[1].replace('"', '') for line in lines[1:] if "," in line]
    with open("output.txt", "w") as out:
        out.write("\n".join(data))

# --- Run classalg and Parse Output ---
def run_algorithm():
    try:
        result = subprocess.run(["python", "classalg.py"], capture_output=True, text=True)
        output = result.stdout.strip()
        if not output:
            output = result.stderr.strip()
        if not output:
            raise Exception("classalg.py produced no output.")
        display_table(output)
        status_label.config(text="✅ Algorithm executed and table updated.", fg="green")
    except Exception as e:
        status_label.config(text=f"❌ Failed: {str(e)}", fg="red")

# --- Parse Output and Populate Treeview Table ---
def display_table(output):
    for row in tree.get_children():
        tree.delete(row)

    lines = output.strip().splitlines()
    for line in lines:
        if ':' not in line:
            continue
        name, class_str = line.split(":", 1)
        classes = class_str.strip().split(", ")
        class_dict = {}
        for cls in classes:
            if "(Block" in cls:
                try:
                    title, block_info = cls.rsplit(" (Block ", 1)
                    block_num = int(block_info.strip(")"))
                    class_dict[block_num] = title
                except ValueError:
                    continue
        ordered_classes = [class_dict.get(i, "") for i in range(1, 6)]
        tree.insert("", "end", values=[name.strip()] + ordered_classes)

# --- UI Layout ---
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

dark_mode_button = tk.Button(frame_top, text="🌙 Dark Mode", width=12, command=toggle_dark_mode)
dark_mode_button.grid(row=0, column=0, padx=5)

open_button = tk.Button(frame_top, text="📂 Open CSV", width=20, command=open_file_dialog)
open_button.grid(row=0, column=1, padx=10)

process_button = tk.Button(frame_top, text="⚙️ Run Algorithm", width=20, command=run_algorithm)
process_button.grid(row=0, column=2, padx=10)

selected_file_label = tk.Label(root, text="No file selected.", font=("Arial", 10))
selected_file_label.pack()

# --- Treeview Table ---
columns = ["Student", "Block 1", "Block 2", "Block 3", "Block 4", "Block 5"]
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

x_scroll = tk.Scrollbar(tree_frame, orient="horizontal")
x_scroll.pack(side="bottom", fill="x")

y_scroll = tk.Scrollbar(tree_frame, orient="vertical")
y_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
tree.pack(fill=tk.BOTH, expand=True)

x_scroll.config(command=tree.xview)
y_scroll.config(command=tree.yview)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180, anchor="w")

status_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
status_label.pack()

# --- Start Light Mode ---
toggle_dark_mode()  # flip to dark
toggle_dark_mode()  # flip back to light (default)

# --- Start Application ---
root.mainloop()
