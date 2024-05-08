#Módulo com as funções que permitem o funcioamento do login bem como o armazenamento dos dados do utilizador

import tkinter as tk
from tkinter import messagebox

import os
from datetime import datetime

from celulas import  *
from funcs import initialize_gui
from user import set_username


# Define the username and password
#USERNAME = "admin"
#PASSWORD = "admin"



# File path for user credentials
CREDENTIALS_FILE_PATH = "Parameters/users.txt"


def load_credentials():
    credentials = {}
    with open(CREDENTIALS_FILE_PATH, "r") as file:
        for line in file:
            username, password = line.strip().split(":")
            credentials[username] = password
    return credentials




def login_success(root):
    # Hide the login frame
    root.login_frame.pack_forget()
    # Initialize the GUI
    initialize_gui(root,10)


def login(root, username_entry, password_entry):
    username = set_username(username_entry.get())
    password = password_entry.get()

    credentials = load_credentials()

    if username in credentials and credentials[username] == password:
        login_success(root)
    else:
        messagebox.showerror("Erro no Login", "Nome de utilizador ou palavra-passe inválidos")


def create_login_frame(root):
    
    global log_img
    
    root.title("Início de sessão")
    root.geometry("1920x1080")
    
    root.login_frame = tk.Frame(root, background="#202020")
    root.login_frame.pack()
        
    log_img = tk.PhotoImage(file = "log.png")
    log_img_label = tk.Label(image = log_img, height = 50, width = 50) 
    

    inicio = tk.Label(root.login_frame, image=log_img,compound="left", text="Início de Sessão", font=("Arial 33 bold"), bg ="#202020", fg="white", justify="center")
    inicio.grid(row=0, columnspan=3, pady=50)
    
    # Create labels and entries for username and password
    username_label = tk.Label(root.login_frame, text="Nome de Usuário:", font =("Arial 18 bold"), fg= "white", background ="#202020")
    username_label.grid(row=1, column=0, padx=0, pady=20)
    root.username_entry = tk.Entry(root.login_frame, bd=0, font=("Arial 18"))
    root.username_entry.grid(row=1, column=1, padx=5, pady=20)

    password_label = tk.Label(root.login_frame, text="Palavra-passe:", font =("Arial 18 bold"), fg= "white", background ="#202020")
    password_label.grid(row=2, column=0, padx=0, pady=20)
    root.password_entry = tk.Entry(root.login_frame, show="•", bd=0, font=("Arial 18"))
    root.password_entry.grid(row=2, column=1, padx=5, pady=20)

    # Create login button
    login_button = tk.Button(root.login_frame, text="Entrar", font = ("Arial 18 bold"), fg ="#202020", background="SeaGreen3", activebackground="SeaGreen2", highlightthickness = 0, bd=0, command=lambda: login(root, root.username_entry, root.password_entry))
    login_button.grid(row=3, columnspan=2, pady=50)


def on_exit(username):
    current_time = datetime.now().strftime("%Y-%m-%d%H-%M-%S")
    directory = f"exitlogs/{username}"
    filename = f"{directory}/{username}{current_time}.txt"

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    with open(filename, "w") as file:
        for cell_number, values in cell_values.items():
            number1_value = values.get("number1", 10)
            number2_value = values.get("number2", 20)
            file.write(f"cell {cell_number} : temperature set to [ {number1_value} ; {number2_value} ]\n")
        file.write("\nProgram exited at: " + str(datetime.now()))