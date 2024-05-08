import tkinter as tk
from tkinter import messagebox
import pickle
import atexit
import os
from datetime import datetime

# Dictionary to store the values for each cell
cell_values = {}

# File path to store the cell values
FILE_PATH = "Parameters/cell_values.pickle"

# File path for user credentials
CREDENTIALS_FILE_PATH = "Parameters/users.txt"

# Define the username and password
#USERNAME = "admin"
#PASSWORD = "admin"

# Initialize root as a global variable
root = tk.Tk()

def send_message(message):
    print("Message sent:", message)

def initialize_cell_values(num_cells):
    global cell_values
    for i in range(1, num_cells + 1):
        cell_values[i] = {"number1": 10, "number2": 20}

def load_cell_values():
    try:
        with open(FILE_PATH, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def save_cell_values():
    with open(FILE_PATH, "wb") as file:
        pickle.dump(cell_values, file)

def load_credentials():
    credentials = {}
    with open(CREDENTIALS_FILE_PATH, "r") as file:
        for line in file:
            username, password = line.strip().split(":")
            credentials[username] = password
    return credentials

def initialize_gui(num_cells):
    # Load cell values from file
    global cell_values
    cell_values = load_cell_values()

    # Initialize the cell values dictionary if it's empty
    if not cell_values:
        initialize_cell_values(num_cells)
    
    # Create the main window
    root.title("Main Page")

    # Set the window size
    root.geometry("800x450")  # Set the width and height of the window

    # Function to create new page within the same window
    def create_new_page_wrapper(cell_number):
        create_new_page(root, main_frame, cell_number)

    # Create the main frame
    main_frame = tk.Frame(root)
    main_frame.pack()

    # Create the buttons for cells
    for i in range(num_cells):
        cell_button = tk.Button(main_frame, text=f"Cell {i+1}", command=lambda i=i: create_new_page_wrapper(i+1))
        cell_button.pack(pady=5)

    # Run the GUI
    root.mainloop()

def login_success():
    # Hide the login frame
    login_frame.pack_forget()
    # Initialize the GUI
    initialize_gui(10)

def login():
    username = username_entry.get()
    password = password_entry.get()

    credentials = load_credentials()

    if username in credentials and credentials[username] == password:
        login_success()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

def create_login_frame(root):
    global login_frame, username_entry, password_entry

    login_frame = tk.Frame(root)
    login_frame.pack()

    # Create labels and entries for username and password
    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create login button
    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, columnspan=2, pady=5)

def create_new_page(root, frame, cell_number):
    # Hide the main frame
    frame.pack_forget()

    # Create a new frame for the new page
    new_frame = tk.Frame(root)
    new_frame.pack()

    # Retrieve the stored values or set defaults
    number1_value = cell_values.get(cell_number, {}).get("number1", 10)
    number2_value = cell_values.get(cell_number, {}).get("number2", 20)

    # Variables to store the numbers
    number1 = tk.IntVar(value=number1_value)
    number2 = tk.IntVar(value=number2_value)

    # Functions to update the numbers
    def increase_number1():
        number1.set(number1.get() + 1)
        send_message(f"min- {number1.get()} cell- {cell_number}")

    def decrease_number1():
        number1.set(number1.get() - 1)
        send_message(f"min- {number1.get()} cell- {cell_number}")

    def increase_number2():
        number2.set(number2.get() + 1)
        send_message(f"max- {number2.get()} cell- {cell_number}")

    def decrease_number2():
        number2.set(number2.get() - 1)
        send_message(f"max- {number2.get()} cell- {cell_number}")

    # Create two numbers
    number1_label = tk.Label(new_frame, textvariable=number1, font=("Arial", 24))
    number1_label.grid(row=0, column=0, padx=100, pady=100)

    number2_label = tk.Label(new_frame, textvariable=number2, font=("Arial", 24))
    number2_label.grid(row=0, column=1, padx=50, pady=10)

    # Create buttons for number 1
    plus_button1 = tk.Button(new_frame, text="+", command=increase_number1)
    plus_button1.grid(row=1, column=0, padx=10, pady=5)
    minus_button1 = tk.Button(new_frame, text="-", command=decrease_number1)
    minus_button1.grid(row=2, column=0, padx=10, pady=5)

    # Create buttons for number 2
    plus_button2 = tk.Button(new_frame, text="+", command=increase_number2)
    plus_button2.grid(row=1, column=1, padx=10, pady=5)
    minus_button2 = tk.Button(new_frame, text="-", command=decrease_number2)
    minus_button2.grid(row=2, column=1, padx=10, pady=5)

    # Back button to return to main frame
    back_button = tk.Button(new_frame, text="Back", command=lambda: return_to_main(frame, new_frame, cell_number, number1, number2))
    back_button.grid(row=3, columnspan=2, pady=10)

def update_cell_values(cell_number, number1_value, number2_value):
    if cell_number not in cell_values:
        cell_values[cell_number] = {}
    cell_values[cell_number]["number1"] = number1_value
    cell_values[cell_number]["number2"] = number2_value
    save_cell_values()

def return_to_main(main_frame, new_frame, cell_number, number1, number2):
    # Store the values when returning to main frame
    update_cell_values(cell_number, number1.get(), number2.get())

    # Hide the new frame
    new_frame.pack_forget()

    # Display the main frame
    main_frame.pack()

def on_exit(username):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = f"exit_logs/{username}"
    filename = f"{directory}/{username}_{current_time}.txt"

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    with open(filename, "w") as file:
        for cell_number, values in cell_values.items():
            number1_value = values.get("number1", 10)
            number2_value = values.get("number2", 20)
            file.write(f"cell {cell_number} : temperature set to [ {number1_value} ; {number2_value} ]\n")
        file.write("\nProgram exited at: " + str(datetime.now()))


atexit.register(on_exit)



def create_main_page():
    # Create the main window
    root.title("Main Page")

    # Set the window size
    root.geometry("800x450")  # Set the width and height of the window

    # Create the main frame
    main_frame = tk.Frame(root)
    main_frame.pack()

    # Create the buttons for cells
    for i in range(10):
        cell_button = tk.Button(main_frame, text=f"Cell {i+1}", command=lambda i=i: create_new_page(root, main_frame, i+1))
        cell_button.pack(pady=5)

    # Run the GUI
    root.mainloop()



# Create login frame within the main window
create_login_frame(root)
root.mainloop()




