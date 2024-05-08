import tkinter as tk
from tkinter import messagebox

import os
from datetime import datetime

username = ""

def get_username():
    global username
    return username

def set_username(new_username):
    global username
    username = new_username
    return username