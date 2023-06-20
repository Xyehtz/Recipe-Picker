import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet
import sys
import os


""" This function will do the following:
    1. Obtain the relative path of the assets, fonts and database used on the application
    2. Try to obtain the file where the executable file is stored
    3. If an error occurs trying to obtain the file path it will be captured
    4. Finally obtain the file path """

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Declare the background color

bgColor = "#9b5dc7"

# Add the fonts that will be used, using Pyglet

pyglet.font.add_file(resource_path("fonts/Ubuntu-Bold.ttf"))
pyglet.font.add_file(resource_path("fonts/Shanti-Regular.ttf"))


# Destroy a frame if the user is in a different one or is about to open a new one

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


""" Connect to the SQLite3 database and obtain:
        1. All the recipes titles
        2. Randomly select one of the recipes titles
        3. Obtain the name, quantity and unit of the selected recipe
        4. Close the connection and retunr the information of the recipe"""

def fetch_db():
    connection = sqlite3.connect(resource_path("data/recipes.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT title, primary_key FROM recipes")
    all_titles = cursor.fetchall()
    
    idx = random.randint(0, len(all_titles) -1)
    
    recipe_name = all_titles[idx]
    cursor.execute("SELECT name, qty, unit FROM ingredients WHERE recipe_key=:k;", {"k": idx})
    table_records = cursor.fetchall()

    connection.close()
    return recipe_name, table_records


""" Define a new funtion that will pre process all the ingredients,
firts obtain the information stored inside of recipe_name and table_records """

def pre_process(recipe_name, table_records):
    title = recipe_name[0]

    # Create an array where all the ingredients will be stored

    ingredients = []

    # Obtain the name, unit and quantity

    for i in table_records:
        name = i[0]
        unit = i[2]

        # For the quantity make sure that indeed is a float
        if type(i[1] == float):
            qty = i[1]
        else:
            qty = i[1]

        """ Check for the information stored inside of quantity
            if quantity doesn't have any type of information stored just append the name"""

        if qty == None:
            ingredients.append(name)

        # If quantity has a value but unit doesn't just convert to string the quantity and append it to the name

        elif unit == None:
            ingredients.append(f"{str(qty)} {name}")

        # If both quantity and unit have a value append them and the name\

        else:
            ingredients.append(f"{str(qty)} {str(unit)} of {name}")
        
    # Return the title and the ingredients

    return title, ingredients

# Load the first frame, this will appear when the user opens up the app

def load_frame1():

    # Clear the widgets inside of the frame 2 if the user had oppened it before

    clear_widgets(frame2)

    # Load frame1 and put it above every other frame

    frame1.tkraise()
    frame1.pack_propagate(False)
    
    # Create widgets
    # This widget will contain the logo image for the frame1

    logo_img = ImageTk.PhotoImage(
        file=resource_path("assets/RRecipe_logo.png"))
    logo_widget = tk.Label(
        frame1,
        image=logo_img,
        bg=bgColor)
    logo_widget.image = logo_img
    logo_widget.pack()
    
    # Create the text that the user will see below the image

    tk.Label(
        frame1,
        text="Ready for your random recipe?",
        bg=bgColor,
        fg="white",
        font=("Shanti", 14),
    ).pack()
    
    # Create the button that will load frame2

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


# Create the function to load the frame2

def load_frame2():

    # Clear every widget inside the frame1

    clear_widgets(frame1)

    # Load the frame2 and put it above every other frame

    frame.tkraise()

    # Obtain the recipe title and ingredients from the SQLite database

    recipe_name, table_records = fetch_db()
    title, ingredients = pre_process(recipe_name, table_records)
    
    # Create a new widget with a new type of image

    logo_img = ImageTk.PhotoImage(
        file=resource_path("assets/RRecipe_logo_bottom.png"))
    logo_widget = tk.Label(
        frame2,
        image=logo_img,
        bg=bgColor)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
    # Create a label that will show the title of the recipe

    tk.Label(
        frame2,
        text=title,
        bg=bgColor,
        fg="white",
        font=("Ubuntu", 20),
    ).pack(pady=25)
    
    # Iterate through all the ingredients and display them on the application

    for i in ingredients:
        tk.Label(
            frame,
            text=i,
            bg="#79489c",
            fg="white",
            font=("Ubuntu", 12),
        ).pack(fill="both")
        
    # Create a button for the users to load the frame1 and repeat the process

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

# Set title and the positon of the window

root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

# Frame widget of the application

frame1 = tk.Frame(root, width=500, height=600, bg=bgColor)
frame2 = tk.Frame(root, bg=bgColor)

# Create the grid for the two frames

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")
    
# Start the application loading frame1, the app wont close until the user closes it

load_frame1()
root.mainloop()