from customtkinter import *


def hide_pregnant(choice):
    if choice == "Female":
        checkbox.place(relx=0.85, rely=0.65, anchor=CENTER)  # Show the checkbox
    else:
        checkbox.place_forget()  # Hide the checkbox


def validate_age(event=None):
    age = Textbox1.get()
    if age:
        if age.isdigit() and int(age) in range(18, 80):
            vlabel1.configure(
                text=f"Valid age: {age}",
                text_color="green",
            )
            return True
        else:
            vlabel1.configure(
                text="Age must be a number between 18 and 80",
                text_color="red",
            )
            return False
    else:
        vlabel1.configure(
            text="Entry is empty",
            text_color="red",
        )
        return False


def validate_height(event=None):
    height = Textbox2.get()
    if height:
        if height.isdigit() and int(height) in range(45, 271):
            vlabel2.configure(
                text=f"Valid height: {height} cm",
                text_color="green",
            )
            return True
        else:
            vlabel2.configure(
                text="Height must be a number between 45 and 270 cm",
                text_color="red",
            )
            return False
    else:
        vlabel2.configure(
            text="Height entry is empty",
            text_color="red",
        )
        return False


def validate_weight(event=None):
    weight = Textbox3.get()
    if weight:
        if weight.isdigit() and int(weight) in range(30, 301):
            vlabel3.configure(
                text=f"Valid weight: {weight} kg",
                text_color="green",
            )
            return True
        else:
            vlabel3.configure(
                text="Weight must be a number between 30 and 300 kg",
                text_color="red",
            )
            return False
    else:
        vlabel3.configure(
            text="Weight entry is empty",
            text_color="red",
        )
        return False


App = CTk()
App.wm_title("BMI CALCULATOR")
App.geometry("400x300")
set_appearance_mode("light")

# Make the window non-resizable
App.resizable(False, False)

# Checkbox for pregnant user (initially hidden)
checkbox = CTkCheckBox(master=App, text="Pregnant", fg_color='orange', hover_color='#ffcf40', text_color='black', border_width=2, border_color='black', corner_radius=8)
checkbox.place_forget()

# Gender drop-down selection
combobox = CTkComboBox(master=App, values=["Male", "Female"], text_color='black', dropdown_fg_color='black', command=hide_pregnant)
combobox.place(relx=0.5, rely=0.65, anchor=CENTER)

# Labels for the textboxes
Label1 = CTkLabel(App, text='Age', text_color='black', font=('sans-serif', 12))
Label2 = CTkLabel(App, text='Height', text_color='black', font=('sans-serif', 12))
Label3 = CTkLabel(App, text='Weight', text_color='black', font=('sans-serif', 12))

# Label for validation messages
vlabel1 = CTkLabel(App, text='', text_color='black', font=('sans-serif', 12))
vlabel1.place(relx=0.5, rely=0.10, anchor=CENTER)
vlabel2 = CTkLabel(App, text='', text_color='black', font=('sans-serif', 12))
vlabel2.place(relx=0.5, rely=0.273, anchor=CENTER)
vlabel3 = CTkLabel(App, text='', text_color='black', font=('sans-serif', 12))
vlabel3.place(relx=0.5, rely=0.423, anchor=CENTER)

# Textboxes for input from the user
Textbox1 = CTkEntry(App, width=200, height=25, text_color='black', placeholder_text='Enter your age', border_color='black', placeholder_text_color='black')
Textbox2 = CTkEntry(App, width=200, height=25, text_color='black', placeholder_text='Enter your height', border_color='black', placeholder_text_color='black')
Textbox3 = CTkEntry(App, width=200, height=25, text_color='black', placeholder_text='Enter your weight', border_color='black', placeholder_text_color='black')

# Bind the validation functions to the respective textboxes
Textbox1.bind("<KeyRelease>", validate_age)
Textbox2.bind("<KeyRelease>", validate_height)
Textbox3.bind("<KeyRelease>", validate_weight)

# Place the labels
Label1.place(relx=0.1, rely=0.15, anchor=NW)
Label2.place(relx=0.1, rely=0.30, anchor=NW)
Label3.place(relx=0.1, rely=0.45, anchor=NW)

# Place the textboxes
Textbox1.place(relx=0.5, rely=0.20, anchor=CENTER)
Textbox2.place(relx=0.5, rely=0.35, anchor=CENTER)
Textbox3.place(relx=0.5, rely=0.50, anchor=CENTER)

# Calculate button
Button = CTkButton(master=App, text='Calculate', corner_radius=8, hover_color='orange', border_width=0, fg_color="#ffcf40", text_color="black")
Button.place(relx=0.5, rely=0.80, anchor=CENTER)

App.mainloop()
