from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import os.path
import subprocess
import datetime

# Tkinter window setup
gui = tk.Tk()
gui.title("To-Do")
gui.geometry("700x500")

gui.columnconfigure(1, weight=1)
gui.rowconfigure(1, weight=1)

# Initialize the task list
task_list = []

txt_path = "./tasks.txt"

check_file = os.path.isfile(txt_path)

if check_file == True:
    with open("tasks.txt", "r") as tasks:
        data = tasks.read()
        task_list = data.splitlines()

task_box_list = tk.StringVar(value=task_list)

new_task_var = tk.StringVar()


# Adds the input from text box to task_list
def add_task():
    new_task = new_task_var.get()
    task_list.append(new_task)
    task_box.insert(END, task_list[-1])

    # Save list items to .txt file
    txt_task = f"{new_task}\n"

    with open("tasks.txt", "a") as tasks:
        tasks.write(txt_task)

    # Clear the entry field
    add_task_ent.delete(0, END)


def delete_task():
    # Get index of selected task
    selected = task_box.curselection()
    # get task index from tuple
    task_index = selected[0]
    task_str = f"{task_list[task_index]}\n"
    del_text = ""

    # Delete task from list
    del task_list[task_index]

    with open(r"tasks.txt", "r") as file:
        data = file.read()
        data = data.replace(task_str, del_text)

    with open(r"tasks.txt", "w") as file:
        file.write(data)

    # Delete task from listbox
    task_box.delete(selected)


def complete_task():
    selected = task_box.curselection()
    task_index = selected[0]
    task_str = f"{task_list[task_index]}\n"
    del_text = ""

    now = datetime.datetime.now()
    current_time = now.replace(microsecond=0)

    comp_str = f"Completed {current_time}:\n{task_str}"

    # Add task to text file of completed tasks
    with open("completed.txt", "a") as tasks:
        tasks.write(comp_str)

    # Delete task from list
    del task_list[task_index]

    with open(r"tasks.txt", "r") as file:
        data = file.read()
        data = data.replace(task_str, del_text)

    with open(r"tasks.txt", "w") as file:
        file.write(data)

    # Delete task from listbox
    task_box.delete(selected)


def view_completed():
    os_type = os.name
    # Windows command
    if os_type == "nt":
        os.system("notepad.exe completed.txt")
    # Linux command
    elif os_type == "posix":
        # os.system("xed completed.txt")
        subprocess.run(["xdg-open", "completed.txt"])
    else:
        os.startfile("completed.txt")


# Label frame for "Add Task" entry box
add_task_frm = ttk.LabelFrame(gui, text="Add Task")
add_task_frm.grid(row=0, column=1, padx=10, pady=10)

# Entry box for adding a new task
add_task_ent = ttk.Entry(add_task_frm, textvariable=new_task_var, width=60)
add_task_ent.grid(row=0, column=1, padx=10, pady=10)

# Add button to update the list and listbox with the new text entry
add_btn = ttk.Button(add_task_frm, text="Add", command=add_task)
add_btn.grid(row=0, column=2, padx=10, pady=10)

# Set up the listbox
task_box = tk.Listbox(gui, height=17, width=80, listvariable=task_box_list)
task_box.grid(sticky="N", row=1, column=1, padx=10, pady=10)

# Set up delete frame
del_frm = ttk.Frame(gui, height=10, width=20)
del_frm.grid(sticky="N", row=2, column=1, padx=10, pady=10)

# Button to view completed tasks
view_complete_btn = ttk.Button(
    del_frm, text="View Completed\nTasks", command=view_completed
)
view_complete_btn.pack(side=RIGHT, padx=20, pady=10)

# Button to delete elements from listbox.
del_btn = ttk.Button(del_frm, text="Delete\nTask", command=delete_task)
del_btn.pack(side=RIGHT, padx=20, pady=10)

# Button to mark tasks as completed
cmp_btn = ttk.Button(del_frm, text="Complete\nTask", command=complete_task)
cmp_btn.pack(side=LEFT, padx=20, pady=10)


# Function for adding new tasks with the Enter key
def enter_task(event):
    add_task()


# Use the Enter key to add new tasks in the entry box
gui.bind("<Return>", enter_task)


gui.mainloop()
