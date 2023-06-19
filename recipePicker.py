import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

bgColor = "#9b5dc7"

pyglet.font.add_file(resource_path("Github clone\\RandomRecipePicker\\complete_project_WINDOWS\\fonts\\Ubuntu-Bold.ttf"))
pyglet.font.add_file(resource_path("Github clone\\RandomRecipePicker\\complete_project_WINDOWS\\fonts\\Shanti-Regular.ttf"))

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect(resource_path("Github clone\\RandomRecipePicker\\complete_project_WINDOWS\\data\\recipes.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    allTables = cursor.fetchall()
    
    idx = random.randint(0, len(allTables) -1)
    
    tableName = allTables[idx][1]
    cursor.execute("SELECT * FROM " + tableName + ";")
    tableRecords = cursor.fetchall()
    
    connection.close()
    return tableName, tableRecords

def pre_process(tableName, tableRecords):
    title = tableName[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])
    
    ingredients = []
    
    for i in tableRecords:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)
        
    return title, ingredients

def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    
    # Create widgets
    
    logoImg = ImageTk.PhotoImage(
        file=resource_path("Github clone\\RandomRecipePicker\\complete_project_WINDOWS\\assets\\RRecipe_logo.png"))
    logoWidget = tk.Label(
        frame1,
        image=logoImg,
        bg=bgColor)
    logoWidget.image = logoImg
    logoWidget.pack()
    
    tk.Label(
        frame1,
        text="Ready for your random recipe?",
        bg=bgColor,
        fg="white",
        font=("Shanti", 14),
    ).pack()
    
    tk.Button(
        frame1,
        text="SHUFFLE",
        font=("Ubuntu", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: load_frame2()
    ).pack(pady=20)

def load_frame2():
    clear_widgets(frame1)
    frame.tkraise()
    tableName, tableRecords = fetch_db()
    title, ingredients = pre_process(tableName, tableRecords)
    
    logoImg = ImageTk.PhotoImage(
        file=resource_path("Github clone\\RandomRecipePicker\\complete_project_WINDOWS\\assets\\RRecipe_logo_bottom.png"))
    logoWidget = tk.Label(
        frame2,
        image=logoImg,
        bg=bgColor)
    logoWidget.image = logoImg
    logoWidget.pack(pady=20)
    
    tk.Label(
        frame2,
        text=title,
        bg=bgColor,
        fg="white",
        font=("Ubuntu", 20),
    ).pack(pady=25)
    
    for i in ingredients:
        tk.Label(
            frame,
            text=i,
            bg="#79489c",
            fg="white",
            font=("Ubuntu", 12),
        ).pack(fill="both")
        
    tk.Button(
        frame2,
        text="BACK",
        font=("Ubuntu", 18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: load_frame1()
    ).pack(pady=20)

# Initialize app
root = tk.Tk()
root.title("Recipe Picker") # Set title

# Set the position of the window
root.eval("tk::PlaceWindow . center")

# Frame widget of the application
frame1 = tk.Frame(root, width=500, height=600, bg=bgColor)
frame2 = tk.Frame(root, bg=bgColor)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")
    
load_frame1()

root.mainloop()