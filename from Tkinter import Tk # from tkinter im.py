import tkinter as tk
import json
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("csv", "*.csv*"), ("All files", "*.*")])
    if file_path:
        selected_file_label.config(text=f"Selected File:\n{file_path}")
        process_file(file_path)
        edit_class()


def process_file(file_path):
    try:
        with open(file_path, 'r+') as file:
            file_contents = file.read()
            file_text.delete(1.0, tk.END)
            temp_file_name = file_path.split("/")[-1]
            # the 3 lines above delete the text in the text box and then add the file name to the text box

            file_text.insert(tk.END, "File \"" + temp_file_name + "\" successfully read.")

        with open('output.txt', 'r+') as file:
            # clear the file contents
            file.truncate(0)
            # remove the first line
            file_contents = file_contents.split("\n", 1)[1]
            # split each line into a list of strings
            file_contents = file_contents.split("\n")
            # remove the everything before the first comma, on each indice
            for i in range(len(file_contents)):
                file_contents[i] = file_contents[i].split(",", 1)[1]
            # add the new list to the file
            for i in range(len(file_contents)):
                file.write(file_contents[i] + "\n")
            

    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")

def edit_class(): # this creates/edits a class and writes it to the classdat.json file
    # with open('classdat.json', 'r+') as file:
    #     # remove everything except " { "classes": { } } "
    #     data = json.loadile)
    #     data = {"classes": {}}
    #     file.seek(0)
    #     json.dump(data, file, indent=4)
    with open('output.txt', 'r+') as file:
        file_content = file.readlines()
    print(file_content)
    print(len(file_content))
    for i in range(len(file_content)):
        with open('classdat.json', 'r+') as file:
            data = json.load(file)
            new_class = {
                # set the name to everything before the first comma, without the ""
                "name": file_content[i].split(",", 1)[0]
                # "prereqs": input("Enter the prerequisites for the new class: "),
                # "MinGrade": input("Enter the minimum grade for the new class(0-3, freshman-senior): "),
                
                # "Blocks": selectBlocks(),
                # "Standards": selectStandards(),
                # "ClassSize": ClassSize(),
                # "Topics": selectTopics()
            }
            data['classes'].update({new_class['name']: new_class})
            file.seek(0)
            json.dump(data, file, indent=4)

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