from customtkinter import *

# ----- Iron Man Theme Colors -----
COLOR_PRIMARY_RED = "#C0392B"
COLOR_PRIMARY_GOLD = "#F1C40F"
COLOR_DARK_ACCENT = "#2C3E50"
COLOR_LIGHT_ACCENT = "#ECF0F1"
COLOR_APP_BG = "#34495E"

COLOR_GOLD_HOVER = "#F39C12"
COLOR_RED_HOVER = "#E74C3C"
COLOR_SUCCESS_GREEN = "#2ECC71"
COLOR_ERROR_RED = "#E74C3C"
COLOR_PLACEHOLDER_LIGHT_GOLD = "#FAD7A0"

# ----- App Setup -----
App = CTk()
App.wm_title("bmi calculator")
App.geometry("600x300")
App.configure(fg_color=COLOR_APP_BG)
set_appearance_mode("dark")

# ----- Validation Functions -----
def validate_age(event=None):
    age = Textbox1.get()
    if age and age.isdigit() and 18 <= int(age) < 80:
        vlabel1.configure(text=f"Valid age: {age}", text_color=COLOR_SUCCESS_GREEN)
        return True
    else:
        msg = ("Entry is empty" if not age else
               "Age must be a number between 18 and 80")
        vlabel1.configure(text=msg, text_color=COLOR_ERROR_RED)
        return False

def validate_height(event=None):
    height = Textbox2.get()
    if height and height.isdigit() and 45 <= int(height) < 271:
        vlabel2.configure(text=f"Valid height: {height} cm", text_color=COLOR_SUCCESS_GREEN)
        return True
    else:
        msg = ("Height entry is empty" if not height else
               "Height must be 45–270 cm")
        vlabel2.configure(text=msg, text_color=COLOR_ERROR_RED)
        return False

def validate_weight(event=None):
    weight = Textbox3.get()
    if weight and weight.isdigit() and 30 <= int(weight) < 301:
        vlabel3.configure(text=f"Valid weight: {weight} kg", text_color=COLOR_SUCCESS_GREEN)
        return True
    else:
        msg = ("Weight entry is empty" if not weight else
               "Weight must be 30–300 kg")
        vlabel3.configure(text=msg, text_color=COLOR_ERROR_RED)
        return False

# ----- BMI Calculation -----
def calculate_bmi():
    valid_age = validate_age()
    valid_height = validate_height()
    valid_weight = validate_weight()

    if not (valid_age and valid_height and valid_weight):
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "Please correct the input errors.")
        Output.configure(state='disabled')
        return

    if combobox.get() == "Female" and checkbox.get() == 1:
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "BMI calculation is not eligible for pregnant women.")
        Output.configure(state='disabled')
        return

    h_cm = int(Textbox2.get())
    w_kg = int(Textbox3.get())
    h_m = h_cm / 100
    bmi = w_kg / (h_m * h_m)

    category = ("Underweight" if bmi < 18.5 else
                "Normal weight" if bmi < 25 else
                "Overweight" if bmi < 30 else
                "Obese")

    report = (
        f'Age: {Textbox1.get()} years\n'
        f'Gender: {combobox.get()}\n'
        f'Height: {Textbox2.get()} cm\n'
        f'Weight: {Textbox3.get()} kg\n'
        f'BMI : {bmi:.2f} ({category})\n'
    )

    Output.configure(state='normal')
    Output.delete("0.0", "end")
    Output.insert("0.0", report)
    Output.configure(state='disabled')

# ----- UI Element Setup -----
App.resizable(False, False)
FONT = ("Futura", 12)

# Checkbox for 'Pregnant' option
checkbox = CTkCheckBox(
    master=App,
    text="Pregnant",
    fg_color=COLOR_PRIMARY_GOLD,
    hover_color=COLOR_GOLD_HOVER,
    border_width=3,
    border_color=COLOR_PRIMARY_RED,
    text_color=COLOR_PRIMARY_GOLD,
    font=FONT
)
checkbox.place(relx=0.42, rely=0.65, anchor=CENTER)

# Combobox for gender selection
combobox = CTkComboBox(
    master=App,
    values=["Male", "Female"],
    fg_color=COLOR_PRIMARY_RED,
    dropdown_fg_color=COLOR_PRIMARY_RED,
    dropdown_hover_color=COLOR_RED_HOVER,
    dropdown_text_color=COLOR_LIGHT_ACCENT,
    button_color=COLOR_PRIMARY_GOLD,
    button_hover_color=COLOR_GOLD_HOVER,
    text_color=COLOR_LIGHT_ACCENT,
    border_color=COLOR_PRIMARY_GOLD,
    font=FONT,
)
combobox.place(relx=0.2, rely=0.65, anchor=CENTER)

# Labels for input fields
Label1 = CTkLabel(App, text='Age', text_color=COLOR_PRIMARY_GOLD, font=FONT)
Label2 = CTkLabel(App, text='Height', text_color=COLOR_PRIMARY_GOLD, font=FONT)
Label3 = CTkLabel(App, text='Weight', text_color=COLOR_PRIMARY_GOLD, font=FONT)

# Validation labels (to show if input is valid or not)
vlabel1 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG)
vlabel2 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG)
vlabel3 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG)

for lbl, y_pos in [(vlabel1, .123), (vlabel2, .273), (vlabel3, .423)]:
    lbl.place(relx=0.3, rely=y_pos, anchor=CENTER)

# Entry fields for user input
Textbox1 = CTkEntry(
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    placeholder_text='Enter your age',
    placeholder_text_color=COLOR_PLACEHOLDER_LIGHT_GOLD,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8
)
Textbox2 = CTkEntry(
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    placeholder_text='Enter your height in cm',
    placeholder_text_color=COLOR_PLACEHOLDER_LIGHT_GOLD,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8
)
Textbox3 = CTkEntry(
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    placeholder_text='Enter your weight in kg',
    placeholder_text_color=COLOR_PLACEHOLDER_LIGHT_GOLD,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8
)

Textbox1.bind("<KeyRelease>", validate_age)
Textbox2.bind("<KeyRelease>", validate_height)
Textbox3.bind("<KeyRelease>", validate_weight)

Label1.place(relx=0.05, rely=0.15, anchor=NW)
Label2.place(relx=0.05, rely=0.30, anchor=NW)
Label3.place(relx=0.05, rely=0.45, anchor=NW)

Textbox1.place(relx=0.3, rely=0.20, anchor=CENTER)
Textbox2.place(relx=0.3, rely=0.35, anchor=CENTER)
Textbox3.place(relx=0.3, rely=0.50, anchor=CENTER)

# Calculate Button
Button = CTkButton(
    master=App,
    text='Calculate BMI',
    fg_color=COLOR_PRIMARY_GOLD,
    hover_color=COLOR_GOLD_HOVER,
    text_color=COLOR_DARK_ACCENT,
    font=FONT,
    corner_radius=8,
    border_width=0
)
Button.configure(command=calculate_bmi)
Button.place(relx=0.3, rely=0.8, anchor=CENTER)

# Output Area
OutputLabel = CTkLabel(App, text='BMI Report', text_color=COLOR_PRIMARY_GOLD, font=FONT)
OutputLabel.place(relx=0.725, rely=0.1, anchor=CENTER)

Output = CTkTextbox(
    master=App,
    width=255, height=170,
    fg_color=COLOR_PRIMARY_RED,
    border_color=COLOR_PRIMARY_GOLD,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8,
)
Output.place(relx=0.725, rely=0.45, anchor=CENTER)
Output.configure(state='disabled')

App.mainloop()