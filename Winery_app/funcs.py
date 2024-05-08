#Módulo que contém as funções que controlam o desempenho principal da aplicação

import tkinter as tk
import os
from celulas import *
from datetime import datetime
import encryption
from user import get_username
from logs_visualization import *


def return_to_main(main_frame, new_frame, cell_number, number1, number2):
    # Store the values when returning to main frame
    update_cell_values(cell_number, number1.get(), number2.get())

    # Hide the new frame
    new_frame.pack_forget()

    # Display the main frame
    main_frame.pack()


def write_log(username, cell_number):
    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log message
    log_message = f"O utilizador {username} editou a temperatura às {current_time} coms os seguintes valores: mínimo- {get_num1_cell_values(cell_number)} máximo- {get_num2_cell_values(cell_number)} cuba- {cell_number}\n"

    if not os.path.exists("Logs"):
        os.makedirs("Logs")  # Create 'Logs' directory if it doesn't exist

    
    # Encrypt log message
    encrypted_log_message = encryption.encrypt_message( log_message.encode())
    
    # Write encrypted log message to log file
    with open("Logs/log.txt", "ab") as file:  # Use 'ab' mode to append binary data
        file.write(encrypted_log_message)



def create_new_page(root, frame, cell_number):
    # Hide the main frame
    frame.pack_forget()
    
    global seta_cima, seta_baixo
    
    seta_cima = tk.PhotoImage(file = "seta_cima.png")
    sc_label = tk.Label(image = seta_cima, height = 102, width = 100)    
    
    seta_baixo = tk.PhotoImage(file = "seta_baixo.png")
    sb_label = tk.Label(image = seta_baixo, height = 102, width = 100)
    
    
    # Create a new frame for the new page
    new_frame = tk.Frame(root, background= "#202020")
    new_frame.pack()
    

    # Retrieve the stored values or set defaults
    #number1_value = get_num1_cell_values(cell_number)
    #number2_value = get_num2_cell_values(cell_number)

    number1_value = get_num1_cell_values(cell_number)
    number2_value = get_num2_cell_values(cell_number)

    def sendMessageToESP32():
        send_message(number1.get(), number2.get())
        update_cell_values(cell_number, number1.get(), number2.get())
        username = get_username()
        write_log(username, cell_number)
        confirm_button.config(state='disabled', relief=tk.SUNKEN)  # Disable button and change appearance
        #return_to_main(frame, new_frame, cell_number, number1, number2)

    # Variables to store the numbers
    number1 = tk.IntVar(value=number1_value)
    number2 = tk.IntVar(value=number2_value)

    # Functions to update the numbers
    def increase_number1():
        number1.set(number1.get() + 1)
        confirm_button.config(state='normal', relief=tk.RAISED)  # Enable button and change appearance

    def decrease_number1():
        number1.set(number1.get() - 1)
        confirm_button.config(state='normal', relief=tk.RAISED)  # Enable button and change appearance

    def increase_number2():
        number2.set(number2.get() + 1)
        confirm_button.config(state='normal', relief=tk.RAISED)  # Enable button and change appearance

    def decrease_number2():
        number2.set(number2.get() - 1)
        confirm_button.config(state='normal', relief=tk.RAISED)  # Enable button and change appearance

    texto1_label = tk.Label(new_frame, text="Temperatura mínima [ºC]", font=("Arial 22 bold"), bg ="#202020", fg="white")
    texto1_label.grid(row=0, column=0, padx=50, pady=100)
    
    texto2_label = tk.Label(new_frame, text="Temperatura máxima [ºC]", font=("Arial 22 bold"), bg ="#202020", fg="white")
    texto2_label.grid(row=0, column=1, padx=50, pady=100)
    
    # Create two numbers
    number1_label = tk.Label(new_frame, textvariable=number1, font=("Arial 40 bold"), bg ="#202020", fg="white")
    number1_label.grid(row=1, column=0, padx=100)

    number2_label = tk.Label(new_frame, textvariable=number2, font=("Arial 40 bold"), bg ="#202020", fg="white")
    number2_label.grid(row=1, column=1, padx=100)


    # Create buttons for number 1
    plus_button1 = tk.Button(new_frame, image=seta_cima,background = "#202020", command=increase_number1, highlightthickness = 0, bd=0, activebackground="#202020")
    plus_button1.grid(row=2, column=0, padx=10, pady=30)
    minus_button1 = tk.Button(new_frame, image=seta_baixo, background = "#202020", command=decrease_number1, highlightthickness = 0, bd=0, activebackground="#202020")
    minus_button1.grid(row=3, column=0, padx=10, pady=10)
    
    # Create buttons for number 2
    plus_button2 = tk.Button(new_frame, image=seta_cima, background = "#202020", command=increase_number2, highlightthickness = 0, bd=0, activebackground="#202020")
    plus_button2.grid(row=2, column=1, padx=10, pady=30)
    minus_button2 = tk.Button(new_frame, image=seta_baixo,background = "#202020", command=decrease_number2, highlightthickness = 0, bd=0, activebackground="#202020")
    minus_button2.grid(row=3, column=1, padx=10, pady=10)


    
    # Confirm button
    confirm_button = tk.Button(new_frame, text="Confirmar", font=("Arial 18 bold"),fg ="#202020", bg="SeaGreen3",activebackground="SeaGreen2", command=sendMessageToESP32, highlightthickness = 0, bd=0)
    confirm_button.grid(row=4, columnspan=2, pady=20)
    confirm_button.config(state='disabled', relief=tk.SUNKEN)  # Disable button and change appearance

    # Back button to return to main frame
    back_button = tk.Button(new_frame, text="Retroceder", font=("Arial 18 bold"),fg ="#202020", bg="dark turquoise", activebackground="turquoise", highlightthickness = 0, bd=0, command=lambda: return_to_main(frame, new_frame, cell_number, number1, number2))
    back_button.grid(row=5, columnspan=2, pady=20)

    # Add a clickable label for logs
    logs_label = tk.Label(new_frame, text="Relatório de registos", fg="pink", cursor="hand2", bg ="#202020", font=("Arial 10"))
    logs_label.grid(row=6, columnspan=2, pady=20)
    logs_label.bind("<Button-1>", lambda event: open_logs(root, new_frame, cell_number))  # Bind the click event to open_logs function




def initialize_gui(root, num_cells):
    
    # Load cell values from file
    global cell_values
    cell_values = load_cell_values()

    #titulo = tk.Label(root, text="Seja bem vindo!", font=("Times New Roman", 40))
    #frase = tk.Label(root, text="Por favor escolha a cuba que pretende efetuar alterações", font=("Times New Roman", 20))
    #titulo.pack(pady=50)
    #frase.pack(pady=5)
    
    imagem = tk.PhotoImage(file = "Cuba.png")
    img_label = tk.Label(image = imagem, height = 150, width = 150)

    #print("Cell values:", cell_values)
    # Initialize the cell values dictionary if it's empty
    if not cell_values:
        initialize_cell_values(num_cells)

    # Create the main window
    root.title("Página Principal")

    # Set the window size
    root.geometry("1920x1080")  # Set the width and height of the window
    
    
    # Function to create new page within the same window
    def create_new_page_wrapper(cell_number):
        create_new_page(root, main_frame, cell_number)

    # Create the main frame
    main_frame = tk.Frame(root, background = "#202020")
    main_frame.pack()

    texto= tk.Label(main_frame, text="Seja bem vindo! Escolha a cuba em que deseja efetuar alterações.", font=("Arial 30 bold"), foreground="white",background = "#202020")
    texto.place(relx=0.5,rely=0.17,anchor="center")
    
    # Create the buttons for cells
    for i in range(num_cells):
        cell_button = tk.Button(main_frame,text=f"Cuba {i+1}", font=("Arial 18 bold"), foreground="white", image = imagem, compound="top", background = "#202020", highlightthickness = 0, bd=0, activebackground="#202020", activeforeground="#FA9E00", command=lambda i=i: create_new_page_wrapper(i+1), height = 200, width = 150)
        cell_button.pack(side= 'left', pady=350, padx=8)

    # Run the GUI
    root.mainloop()


def create_main_page(root):
    global cell_values
    
    
    imagem = tk.PhotoImage(file = "Cuba.png")
    img_label = tk.Label(image = imagem, height = 150, width = 150)
    
 
    # Create the main window
    root.title("Main Page")

    # Set the window size
    root.geometry("800x450")  # Set the width and height of the window
    

    # Create the main frame
    main_frame = tk.Frame(root, background = "#202020")
    main_frame.pack()

    texto= tk.Label(main_frame, text="Bem vindo! Escolha a cuba em que deseja efetuar alterações.", font=("Arial 30 bold"), foreground="white",background = "#202020")
    texto.place(x=700, y=100)
    
    
    # Create the buttons for cells
    for i in range(10):
        cell_button = tk.Button(main_frame, image = imagem, compound="top", text=f"Cuba {i+1}", font=("Arial 12 bold"), foreground="white", background = "#202020", highlightthickness = 0, bd=0, activebackground="#202020",activeforeground="#FA9E00", command=lambda i=i: create_new_page(root, main_frame, i+1), height = 200, width = 150)
        cell_button.pack(side= 'left', pady=350, padx=8)


    # Run the GUI
    root.mainloop()
