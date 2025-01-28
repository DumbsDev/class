import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("csv", "*.csv*"), ("All files", "*.*")])
    if file_path:
        selected_file_label.config(text=f"Selected File:\n{file_path}")
        process_file(file_path)

def process_file(file_path):
    # Implement your file processing logic here
    # For demonstration, let's just display the contents of the selected file
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            file_text.delete(1.0, tk.END)
            temp_file_name = file_path.split("/")[-1]

            file_text.insert(tk.END, "File \"" + temp_file_name + "\" successfully read.")

    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")

root = tk.Tk()
root.title("CSV to JSON Converter")

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack(padx=20, pady=20)

selected_file_label = tk.Label(root, text="Selected File:\n")
selected_file_label.pack()

file_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
file_text.pack(padx=20, pady=20)
# set icon
root.iconbitmap("")

root.mainloop()
