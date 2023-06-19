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

pyglet.font.add_file(resource_path("fonts/Ubuntu-Bold.ttf"))
pyglet.font.add_file(resource_path("fonts/Shanti-Regular.ttf"))


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


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


def pre_process(recipe_name, table_records):
    title = recipe_name[0]
    
    ingredients = []
    
    for i in table_records:
        name = i[0]
        unit = i[2]

        if type(i[1] == float):
            qty = i[1]
        else:
            qty = i[1]
        if qty == None:
            ingredients.append(name)
        elif unit == None:
            ingredients.append(str(qty) + " " + name)
        else:
            ingredients.append(str(qty) + " " + str(unit) + " " + " of " + name)
        
    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    
    # Create widgets
    
    logo_img = ImageTk.PhotoImage(
        file=resource_path("assets/RRecipe_logo.png"))
    logo_widget = tk.Label(
        frame1,
        image=logo_img,
        bg=bgColor)
    logo_widget.image = logo_img
    logo_widget.pack()
    
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
    recipe_name, table_records = fetch_db()
    title, ingredients = pre_process(recipe_name, table_records)
    
    logo_img = ImageTk.PhotoImage(
        file=resource_path("assets/RRecipe_logo_bottom.png"))
    logo_widget = tk.Label(
        frame2,
        image=logo_img,
        bg=bgColor)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
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
root.title("Recipe Picker")  # Set title

# Set the position of the window
root.eval("tk::PlaceWindow . center")

# Frame widget of the application
frame1 = tk.Frame(root, width=500, height=600, bg=bgColor)
frame2 = tk.Frame(root, bg=bgColor)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")
    
load_frame1()

root.mainloop()