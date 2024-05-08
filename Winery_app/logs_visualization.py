
import tkinter as tk
from tkinter import messagebox
import os
from encryption import *


def return_to_cell_page(frame, logs_frame, cell_number):
    # Hide the logs window
    logs_frame.pack_forget()

    # Display the cell frame
    frame.pack()


def show_logs():
    # Define the path to the encrypted log file
    encrypted_log_file = "Logs/log.txt"
    
    # Read the encrypted log file
    with open(encrypted_log_file, "rb") as file:
        encrypted_content = file.read()

    # Decrypt the encrypted content
    decrypted_content = decrypt_message(encrypted_content)

    # Convert the decrypted bytes to string
    log_text = decrypted_content.decode("utf-8")
    return log_text




def open_logs(root, frame, cell_number):

    # Hide the main frame
    frame.pack_forget()

    #Create a new frame for the logs window
    logs_frame = tk.Frame(root,background= "#202020")
    logs_frame.pack()


    # Call the function from the log visualization module
    log_text = show_logs()

    # Create a text widget to display the logs
    log_text_widget = tk.Text(logs_frame, wrap="word",font=("Arial 14 bold"), foreground="white", background="#202020", highlightthickness = 0, bd=0)
    log_text_widget.insert(tk.END, log_text)
    log_text_widget.pack(expand=True, fill="both")
    
    # Create a button to close the logs window
    close_button = tk.Button(logs_frame, text="Fechar",font=("Arial 18 bold"), bg="dark turquoise", activebackground="turquoise", highlightthickness = 0, bd=0, fg="#202020", command=lambda: return_to_cell_page(frame, logs_frame, cell_number))
    close_button.pack()



