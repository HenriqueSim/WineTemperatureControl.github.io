#Módulo com as funções que controlam os parâmetros das células

import pickle
import tkinter as tk
import requests

# Dictionary to store the values for each cell
cell_values = {}

# File path to store the cell values
FILE_PATH = "Parameters/cell_values.pickle"


def send_message(min_temperature, max_temperature):

    # Define the URL of the PHP script
    url = 'http://192.168.26.1/insert_temp.php'
    
    # Define the parameters to be sent in the GET request
    temperature_range = f"[{min_temperature};{max_temperature}]"
    params = {"temperature_range": temperature_range}
    response = requests.get(url, params=params)
    
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Print the response content (which may include JSON or plain text)
        print(response.text)
    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)


def initialize_cell_values(num_cells):
    global cell_values
    for i in range(1, num_cells + 1):
        update_cell_values(i, 10, 20)

def get_num1_cell_values(cell_number):
    return cell_values[cell_number]["number1"]

def get_num2_cell_values(cell_number):
    return cell_values[cell_number]["number2"]

def load_cell_values():
    global cell_values
    try:
        with open(FILE_PATH, "rb") as file:
            cell_values = pickle.load(file)
            return cell_values
    except FileNotFoundError:
        return {}
    

def save_cell_values():
    with open(FILE_PATH, "wb") as file:
        pickle.dump(cell_values, file)


def update_cell_values(cell_number, number1_value, number2_value):
    if cell_number not in cell_values:
        cell_values[cell_number] = {}
    cell_values[cell_number]["number1"] = number1_value
    cell_values[cell_number]["number2"] = number2_value
    save_cell_values()







