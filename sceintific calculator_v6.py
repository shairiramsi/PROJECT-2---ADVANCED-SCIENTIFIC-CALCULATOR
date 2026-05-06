import tkinter as tk
import math
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

# ===== WINDOW =====
root = tk.Tk()
root.title("Advanced Scientific Calculator")
root.geometry("600x350")

root.configure(bg="#0f172a")
expression = ""
memory = 0
mode = "DEG"

# ===== FUNCTIONS =====
display_var = tk.StringVar()   # ✅ MUST come before functions

# now define functions
def update_display(value):
    display_var.set(value)

def press(key):
    global expression
    expression += str(key)
    update_display(expression)

def clear():
    global expression
    expression = ""
    update_display("")

def toggle_power():
    global is_on, expression

    is_on = not is_on
    expression = ""

    if is_on:
        display_var.set("")
        button_refs["ON/OFF"].config(bg="green", text="ON/OFF")
    else:
        display_var.set("OFF")
        button_refs["ON/OFF"].config(bg="red", text="OFF")

def update_button_color(name, color):
    for widget in btn_frame.winfo_children():
        for btn in widget.winfo_children():
            if btn.cget("text") == name:
                btn.config(bg=color, fg="white")
def equal():
    global expression
    try:
        result = str(eval(expression))
        history_list.insert(tk.END, expression + " = " + result)
        update_display(result)
        expression = result
    except:
        update_display("Error")
        expression = ""

def plot_graph():
    try:
        expr = expression.lower()

        # Fix common user mistakes
        expr = expr.replace("^", "**")
        expr = expr.replace("sin", "np.sin")
        expr = expr.replace("cos", "np.cos")
        expr = expr.replace("tan", "np.tan")
        expr = expr.replace("log", "np.log10")
        expr = expr.replace("ln", "np.log")
        expr = expr.replace("sqrt", "np.sqrt")
        expr = expr.replace("exp", "np.exp")

        x = np.linspace(-10, 10, 400)
        y = eval(expr)

        plt.plot(x, y)
        plt.title(f"y = {expression}")
        plt.grid()
        plt.show()

    except:
        messagebox.showerror("Error", "Use format like: sin(x), x**2")


# ✅ Define toggle_history separately
def toggle_history():
    if history_frame.winfo_viewable():
        history_frame.pack_forget()
    else:
        history_frame.pack(side="right", padx=10)


# ===== MATH FUNCTIONS =====
def apply_func(func):
    global expression
    try:
        value = float(expression)
        result = func(value)
        expression = str(result)
        update_display(expression)
    except:
        update_display("Error")
        expression = ""

def apply_trig(func):
    global expression
    try:
        value = float(expression)
        if mode == "DEG":
            value = math.radians(value)
        result = func(value)
        expression = str(result)
        update_display(expression)
    except:
        update_display("Error")
        expression = ""

# ===== EXTRA SCIENTIFIC FUNCTIONS =====

def cube_root():
    apply_func(lambda x: x ** (1/3))

def power10():
    apply_func(lambda x: 10 ** x)

def sinh():
    apply_func(math.sinh)

def cosh():
    apply_func(math.cosh)

def tanh():
    apply_func(math.tanh)

def asin():
    apply_trig(math.asin)

def acos():
    apply_trig(math.acos)

def atan():
    apply_trig(math.atan)

def floor_val():
    apply_func(math.floor)

def ceil_val():
    apply_func(math.ceil)

def round_val():
    apply_func(round)

# Basic scientific
def sqrt(): apply_func(math.sqrt)

def log(): apply_func(math.log10)

def ln(): apply_func(math.log)

def exp(): apply_func(math.exp)

def square(): press("**2")

def cube(): press("**3")

def inverse(): apply_func(lambda x: 1/x)

def abs_val(): apply_func(abs)

# Trigonometry
def sin(): press("sin(")

def cos(): press("cos(")

def tan(): press("tan(")

# Factorial
def factorial():
    global expression
    try:
        expression = str(math.factorial(int(float(expression))))
        update_display(expression)
    except:
        update_display("Error")
        expression = ""

# Constants
def insert_pi(): press(str(math.pi))
def insert_e(): press(str(math.e))

# Percentage
def percent():
    global expression
    try:
        expression = str(float(expression) / 100)
        update_display(expression)
    except:
        update_display("Error")
        expression = ""

# Power
def power(): press("**")

# Mode toggle
def toggle_mode():
    global mode
    mode = "RAD" if mode == "DEG" else "DEG"
    mode_label.config(text=mode)

# ===== MEMORY =====
def memory_add():
    global memory
    try:
        memory += float(expression)
    except:
        pass

def memory_sub():
    global memory
    try:
        memory -= float(expression)
    except:
        pass

def memory_recall():
    update_display(memory)

def memory_clear():
    global memory
    memory = 0

# ===== HISTORY =====
def use_history(event):
    global expression
    try:
        selected = history_list.get(history_list.curselection())
        expression = selected.split("=")[0].strip()
        update_display(expression)
    except:
        pass

# ===== MENU =====
menu_bar = tk.Menu(root)

# ===== FILE MENU =====
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Clear", command=clear)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# ===== MODE MENU =====
mode_menu = tk.Menu(menu_bar, tearoff=0)
mode_menu.add_command(label="Toggle DEG/RAD", command=toggle_mode)
menu_bar.add_cascade(label="Mode", menu=mode_menu)

# ===== GRAPH MENU =====
graph_menu = tk.Menu(menu_bar, tearoff=0)
graph_menu.add_command(label="Plot Graph", command=plot_graph)
menu_bar.add_cascade(label="Graph", menu=graph_menu)

# ===== VIEW MENU =====
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle History", command=toggle_history)
menu_bar.add_cascade(label="View", menu=view_menu)

# ===== HELP MENU =====
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About",
                      command=lambda: messagebox.showinfo("About", "Advanced Scientific Calculator with Graph"))
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# ===== DISPLAY =====
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Arial", 20),
                   bd=10, relief="ridge", justify="right")
display.pack(fill="both", padx=10, pady=10)

mode_label = tk.Label(root, text=mode, bg="#1e1e1e", fg="white")
mode_label.pack()
display.bind("<Key>", lambda e: "break")

# ===== MAIN FRAME =====
main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack()
main_frame.pack(fill="both", expand=True)

tk.Label(root, text="Use x for graph (e.g. sin(x), x**2)",
         bg="#1e1e1e", fg="white").pack()

# ===== BUTTON FRAME =====
btn_frame = tk.Frame(main_frame, bg="#0f172a")
btn_frame.pack(side="left")

btn_style = {"font": ("Arial", 10), "width": 5, "height": 1, "bg": "#2980b9"  , "fg": "white"}

buttons = [
    ['MC', 'MR', 'M+', 'M-', '%'],
    ['ON/OFF', '(', ')', '/', '√'],
    ['7', '8', '9', '*', 'x'],
    ['4', '5', '6', '-', 'x²'],
    ['1', '2', '3', '+', '1/x'],
    ['0', '.', '=', '^', 'exp']
]
is_on = True


button_refs = {}

for row in buttons:
    f = tk.Frame(btn_frame, bg="#0f172a")
    f.pack()

    for btn in row:

        # ===== ACTION =====
        if btn == "=":
            action = equal
        elif btn == "ON/OFF":
            action = toggle_power
        elif btn == "^":
            action = power
        elif btn == "√":
            action = sqrt
        elif btn == "x²":
            action = square
        elif btn == "1/x":
            action = inverse
        elif btn == "n!":
            action = factorial
        elif btn == "exp":
            action = exp
        elif btn == "MC":
            action = memory_clear
        elif btn == "MR":
            action = memory_recall
        elif btn == "M+":
            action = memory_add
        elif btn == "M-":
            action = memory_sub
        elif btn == "%":
            action = percent
        else:
            action = lambda b=btn: press(b)

        # ===== COLOR MAPPING (YOUR COLORS) =====
        if btn.isdigit():
            color = "#1e272e"   # Numbers

        elif btn in ["+", "-", "*", "/", "^"]:
            color = "#ff9f43"   # Operators

        elif btn == "=":
            color = "#2ecc71"   # Equals

        elif btn in ["MC", "MR", "M+", "M-"]:
            color = "#9b59b6"   # Memory

        elif btn in ["√", "x²", "1/x", "n!", "exp", "%"]:
            color = "#3498db"   # Scientific

        elif btn == "ON/OFF":
            color = "#16a085"   # Power (extra nice)

        else:
            color = "#34495e"   # Default

        # ===== CREATE BUTTON =====
        tk_btn = tk.Button(
            f,
            text=btn,
            command=action,
            font=("Arial", 10),
            width=5,
            height=1,
            bg=color,
            fg="white",
            activebackground="#3d3d3d",
            relief="flat"
        )

        tk_btn.pack(side="left", padx=3, pady=3)

        button_refs[btn] = tk_btn
        
# ===== SCIENTIFIC PANEL =====
sci_frame = tk.Frame(main_frame, bg="#0f172a")
sci_frame.pack(side="left", padx=10)

row = 0
col = 0

for text, cmd in [
    ("sin", sin), ("cos", cos), ("tan", tan),
    ("asin", asin), ("acos", acos), ("atan", atan),
    ("log", log), ("ln", ln), ("10^x", power10),
    ("√", sqrt), ("∛", cube_root),
    ("π", insert_pi), ("e", insert_e),
    ("abs", abs_val), ("round", round_val),
    ("floor", floor_val), ("ceil", ceil_val),
    ("sinh", sinh), ("cosh", cosh), ("tanh", tanh),
    ("DEG/RAD", toggle_mode)
]:
    tk.Button(sci_frame, text=text, command=cmd, **btn_style)\
        .grid(row=row, column=col, padx=3, pady=3)

    col += 1
    if col == 3:
        col = 0
        row += 1

# ===== HISTORY =====
history_frame = tk.Frame(main_frame, bg="#236d8d")
history_frame.pack(side="right", padx=10)

tk.Label(history_frame, text="History", bg="#236d8d",
         fg="white", font=("Arial", 12, "bold")).pack()

history_list = tk.Listbox(history_frame, width=15, height=10,
                          bg="#0f172a", fg="white")
history_list.pack()

history_list.bind("<<ListboxSelect>>", use_history)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side="right", fill="y")

history_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_list.yview)

tk.Button(history_frame, text="Clear History",
          command=lambda: history_list.delete(0, tk.END)).pack(pady=5)

# ===== KEYBOARD FUNCTION =====
def backspace():
    global expression
    expression = expression[:-1]
    update_display(expression)

def key_press(event):
    key = event.keysym

    if key in ["Return", "KP_Enter"]:
        equal()

    elif key == "Escape":
        clear()

    elif key == "BackSpace":
        backspace()

    elif event.char in "0123456789x":
        press(event.char)

    elif event.char in "+-*/().":
        press(event.char)
        
        
  
# ===== RUN =====
  
root.bind_all("<KeyPress>", key_press)

def force_focus():
    root.focus_force()
    root.after(50, force_focus)

force_focus()

root.mainloop()