from customtkinter import *
import json
import datetime

# ----- File for Storing History -----
BMI_HISTORY_FILE = "bmi_history.json"

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

# ----- Conversion Functions -----
def feet_inches_to_cm(feet_str, inches_str):
    try:
        feet = float(feet_str)
        inches = float(inches_str)
        if feet < 0 or inches < 0:
            return None # Or raise ValueError("Height values cannot be negative")
        return (feet * 30.48) + (inches * 2.54)
    except ValueError:
        return None

def pounds_to_kg(pounds_str):
    try:
        pounds = float(pounds_str)
        if pounds < 0:
            return None # Or raise ValueError("Weight values cannot be negative")
        return pounds * 0.45359237
    except ValueError:
        return None

# ----- Validation Functions -----
def validate_age(event=None):
    age_str = Textbox1.get()
    if age_str and age_str.isdigit():
        age = int(age_str)
        if 18 <= age <= 99: # Updated age range
            vlabel1.configure(text=f"Valid age: {age}", text_color=COLOR_SUCCESS_GREEN)
            return True
        else:
            vlabel1.configure(text="Age must be 18–99", text_color=COLOR_ERROR_RED)
            return False
    else:
        msg = ("Entry is empty" if not age_str else "Age must be a number")
        vlabel1.configure(text=msg, text_color=COLOR_ERROR_RED)
        return False

def validate_height(event=None):
    unit = height_unit_selector.get()
    if unit == "cm":
        height_cm_str = Textbox2.get()
        if not height_cm_str:
            vlabel2.configure(text="Height entry is empty", text_color=COLOR_ERROR_RED)
            return False
        try:
            height_cm = int(height_cm_str)
            if 45 <= height_cm < 271:
                vlabel2.configure(text=f"Valid height: {height_cm} cm", text_color=COLOR_SUCCESS_GREEN)
                return True
            else:
                vlabel2.configure(text="Height must be 45–270 cm", text_color=COLOR_ERROR_RED)
                return False
        except ValueError:
            vlabel2.configure(text="Height must be a number", text_color=COLOR_ERROR_RED)
            return False
    elif unit == "ft/in":
        feet_str = Textbox2_ft.get()
        inches_str = Textbox2_in.get()
        if not feet_str and not inches_str: # Both empty
             vlabel2.configure(text="Height entries are empty", text_color=COLOR_ERROR_RED)
             return False
        if not feet_str:
            vlabel2.configure(text="Feet entry is empty", text_color=COLOR_ERROR_RED)
            return False
        if not inches_str:
            vlabel2.configure(text="Inches entry is empty", text_color=COLOR_ERROR_RED)
            return False
            
        try:
            feet = int(feet_str)
            inches = int(inches_str) # Allow float for inches? For now int.
            
            valid_feet = 1 <= feet <= 9 # Example range
            valid_inches = 0 <= inches < 12

            if valid_feet and valid_inches:
                vlabel2.configure(text=f"Valid height: {feet} ft {inches} in", text_color=COLOR_SUCCESS_GREEN)
                return True
            elif not valid_feet:
                vlabel2.configure(text="Feet must be 1-9", text_color=COLOR_ERROR_RED)
                return False
            elif not valid_inches:
                vlabel2.configure(text="Inches must be 0-11", text_color=COLOR_ERROR_RED)
                return False
        except ValueError:
            vlabel2.configure(text="Height must be numbers", text_color=COLOR_ERROR_RED)
            return False
    return False # Should not happen

def validate_weight(event=None):
    unit = weight_unit_selector.get()
    weight_str = Textbox3.get()

    if not weight_str:
        vlabel3.configure(text="Weight entry is empty", text_color=COLOR_ERROR_RED)
        return False

    try:
        weight_val = float(weight_str) # Use float for more precision with lbs
        if unit == "kg":
            if 30 <= weight_val < 301: # Standard range in kg
                vlabel3.configure(text=f"Valid weight: {weight_val:.1f} kg", text_color=COLOR_SUCCESS_GREEN)
                return True
            else:
                vlabel3.configure(text="Weight must be 30–300 kg", text_color=COLOR_ERROR_RED)
                return False
        elif unit == "lbs":
            # Approx 30kg to 300kg in lbs: 66 lbs to 661 lbs. Adjust as needed.
            if 66 <= weight_val < 662: 
                vlabel3.configure(text=f"Valid weight: {weight_val:.1f} lbs", text_color=COLOR_SUCCESS_GREEN)
                return True
            else:
                vlabel3.configure(text="Weight must be 66–661 lbs", text_color=COLOR_ERROR_RED)
                return False
    except ValueError:
        vlabel3.configure(text="Weight must be a number", text_color=COLOR_ERROR_RED)
        return False
    return False # Should not happen


# ----- BMI Calculation -----
def calculate_bmi():
    # Ensure validation passes first
    # Call validation functions explicitly to update labels and get their status
    valid_age = validate_age()
    valid_height = validate_height() # This will now use the updated logic
    valid_weight = validate_weight() # This will now use the updated logic

    if not (valid_age and valid_height and valid_weight): # Check results of validation
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "Please correct the input errors highlighted above.")
        Output.configure(state='disabled')
        return

    if combobox.get() == "Female" and checkbox.get() == 1:
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "BMI calculation is not eligible for pregnant women.")
        Output.configure(state='disabled')
        return

    h_cm_metric = 0.0
    w_kg_metric = 0.0
    
    height_unit = height_unit_selector.get()
    weight_unit = weight_unit_selector.get()

    original_height_str = ""
    original_weight_str = ""

    # Process Height
    if height_unit == "cm":
        cm_str = Textbox2.get()
        original_height_str = f"{cm_str} cm"
        try:
            h_cm_metric = float(cm_str)
        except ValueError:
            Output.configure(state='normal'); Output.delete("0.0", "end"); Output.insert("0.0", "Invalid height (cm). Not a number."); Output.configure(state='disabled'); return
    else: # "ft/in"
        ft_str = Textbox2_ft.get()
        in_str = Textbox2_in.get()
        original_height_str = f"{ft_str} ft {in_str} in"
        converted_cm = feet_inches_to_cm(ft_str, in_str)
        if converted_cm is None:
            Output.configure(state='normal'); Output.delete("0.0", "end"); Output.insert("0.0", "Invalid height (ft/in). Not numbers or negative."); Output.configure(state='disabled'); return
        h_cm_metric = converted_cm

    # Process Weight
    if weight_unit == "kg":
        kg_str = Textbox3.get()
        original_weight_str = f"{kg_str} kg"
        try:
            w_kg_metric = float(kg_str)
        except ValueError:
            Output.configure(state='normal'); Output.delete("0.0", "end"); Output.insert("0.0", "Invalid weight (kg). Not a number."); Output.configure(state='disabled'); return
    else: # "lbs"
        lbs_str = Textbox3.get()
        original_weight_str = f"{lbs_str} lbs"
        converted_kg = pounds_to_kg(lbs_str)
        if converted_kg is None:
            Output.configure(state='normal'); Output.delete("0.0", "end"); Output.insert("0.0", "Invalid weight (lbs). Not a number or negative."); Output.configure(state='disabled'); return
        w_kg_metric = converted_kg

    # BMI Calculation using metric values
    if h_cm_metric <= 0 or w_kg_metric <= 0: # Basic check after conversion
        Output.configure(state='normal'); Output.delete("0.0", "end"); Output.insert("0.0", "Height and Weight must be positive values."); Output.configure(state='disabled'); return

    bmi_value = _calculate_bmi_core(h_cm_metric, w_kg_metric) # Now only returns BMI value
    
    age_str = Textbox1.get()
    # Age validation should have already ensured age_str is a valid integer string
    age_int = int(age_str)
    
    bmi_category = _get_age_specific_bmi_category(bmi_value, age_int)

    # Store current calculation details for saving
    App.current_bmi_details = {
        "date": datetime.date.today().isoformat(),
        "age": age_str, # Store as string from textbox
        "gender": combobox.get(),
        "height_str": original_height_str, # Already includes units
        "weight_str": original_weight_str, # Already includes units
        "bmi_value": round(bmi_value, 2), # Round to 2 decimal places for storage
        "bmi_category": bmi_category
    }
    SaveButton.configure(state="normal") # Enable save button
    
    # Report formatting
    height_report_str = original_height_str
    if height_unit == "ft/in":
        height_report_str += f" ({h_cm_metric:.1f} cm)"
    
    weight_report_str = original_weight_str
    if weight_unit == "lbs":
        weight_report_str += f" ({w_kg_metric:.2f} kg)"

    report = (
        f'Age: {age_str} years\n'
        f'Gender: {combobox.get()}\n'
        f'Height: {height_report_str}\n'
        f'Weight: {weight_report_str}\n'
        f'BMI : {bmi_value:.2f} ({bmi_category})\n\n'
        f'*Note: BMI categories can vary by age.'
    )

    Output.configure(state='normal')
    Output.delete("0.0", "end")
    Output.insert("0.0", report)
    Output.configure(state='disabled')
    # Keep SaveButton enabled until a new calculation starts or an error occurs


# ----- Data Persistence Functions -----
def load_records_from_history():
    try:
        with open(BMI_HISTORY_FILE, 'r') as f:
            records = json.load(f)
        return records
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Consider logging this error or informing the user more actively
        # For now, treat as no history if file is corrupted
        return []
    except Exception as e:
        # Catch any other potential I/O errors
        print(f"Error loading history: {e}") # Temporary print for debugging
        return []

def save_record_to_history():
    if not hasattr(App, 'current_bmi_details') or App.current_bmi_details is None:
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "No BMI data to save. Please calculate BMI first.")
        Output.configure(state='disabled')
        return

    new_record = App.current_bmi_details
    
    # Ensure all necessary fields are present before saving
    required_fields = ["date", "age", "gender", "height_str", "weight_str", "bmi_value", "bmi_category"]
    if not all(field in new_record for field in required_fields):
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "Error: Incomplete BMI data for saving.")
        Output.configure(state='disabled')
        return

    records = load_records_from_history()
    records.append(new_record)

    try:
        with open(BMI_HISTORY_FILE, 'w') as f:
            json.dump(records, f, indent=4)
        
        # Update Output to show success, then restore original report after a delay, or add to it
        original_report_content = Output.get("0.0", "end").strip()
        success_message = "\n\n--- Record Saved Successfully! ---"
        
        Output.configure(state='normal')
        # Output.delete("0.0", "end") # Don't delete, append or show temporarily
        Output.insert("end", success_message) 
        Output.configure(state='disabled')
        
        # Optionally, clear App.current_bmi_details or disable SaveButton again
        # App.current_bmi_details = None 
        # SaveButton.configure(state="disabled") # Or leave enabled to save same record again? For now, leave enabled.

    except Exception as e:
        error_message = f"\n\n--- Error saving record: {e} ---"
        Output.configure(state='normal')
        Output.insert("end", error_message)
        Output.configure(state='disabled')


# ----- UI Element Setup -----

    category = ("Underweight" if bmi < 18.5 else
                "Normal weight" if bmi < 25 else
                "Overweight" if bmi < 30 else
                "Obese")

    report = (
        f'Age: {Textbox1.get()} years\n'
        f'Gender: {combobox.get()}\n'
        f'Height: {h_val_for_report}\n' # Use the formatted height string
        f'Weight: {w_val_for_report}\n' # Use the formatted weight string
        f'BMI : {bmi:.2f} ({category})\n'
    )

    Output.configure(state='normal')
    Output.delete("0.0", "end")
    Output.insert("0.0", report)
    Output.configure(state='disabled')

def _calculate_bmi_core(h_cm, w_kg):
    """
    Calculates BMI from metric height and weight.
    h_cm: height in centimeters (float)
    w_kg: weight in kilograms (float)
    Returns: bmi_value (float)
    """
    if h_cm <= 0 or w_kg <= 0:
        return 0.0 # Or raise an error to be caught by caller
    
    h_m = h_cm / 100
    bmi = w_kg / (h_m * h_m)
    return bmi

def _get_age_specific_bmi_category(bmi_value, age):
    """
    Determines BMI category based on BMI value and age.
    bmi_value: float
    age: int
    Returns: category_string (str)
    """
    category = "Not determined"
    if 18 <= age <= 24:
        if bmi_value < 18.5: category = "Underweight"
        elif bmi_value < 23: category = "Normal weight (18-24 yrs)" # 18.5-22.9
        elif bmi_value < 28: category = "Overweight (18-24 yrs)"   # 23-27.9
        else: category = "Obese (18-24 yrs)"                      # >=28
    elif 25 <= age <= 64:
        if bmi_value < 18.5: category = "Underweight"
        elif bmi_value < 25: category = "Normal weight (25-64 yrs)" # 18.5-24.9
        elif bmi_value < 30: category = "Overweight (25-64 yrs)"   # 25-29.9
        else: category = "Obese (25-64 yrs)"                      # >=30
    elif age >= 65: # Covers 65-99 due to validate_age
        if bmi_value < 22: category = "Underweight (65+ yrs)"
        elif bmi_value < 27: category = "Normal weight (65+ yrs)"   # 22-26.9
        elif bmi_value < 30: category = "Overweight (65+ yrs)"   # 27-29.9
        else: category = "Obese (65+ yrs)"                      # >=30
    
    # Fallback for ages outside 18-99 if validation somehow allows, or for unhandled BMI values.
    # Given current validation, age will be within 18-99.
    return category

# ----- UI Element Setup -----
# Main App window and global font
App.resizable(False, False)
FONT = ("Futura", 12)

# --- Callback for unit selectors ---
def update_units_ui(*args):
    # Height
    selected_height_unit = height_unit_selector.get()
    if selected_height_unit == "cm":
        Label2.configure(text="Height (cm)")
        Textbox2.configure(placeholder_text="Enter your height in cm")
        Textbox2.place(relx=0.3, rely=0.35, anchor=CENTER)
        Textbox2_ft.place_forget()
        Textbox2_in.place_forget()
        vlabel2.place(relx=0.3, rely=0.273, anchor=CENTER) # Original position
    else: # "ft/in"
        Label2.configure(text="Height (ft, in)")
        Textbox2_ft.configure(placeholder_text="ft")
        Textbox2_in.configure(placeholder_text="in")
        Textbox2.place_forget()
        Textbox2_ft.place(relx=0.25, rely=0.35, anchor=CENTER) # Adjusted for two fields
        Textbox2_in.place(relx=0.39, rely=0.35, anchor=CENTER) # Adjusted for two fields
        vlabel2.place(relx=0.32, rely=0.273, anchor=CENTER) # Adjusted for two fields

    # Weight
    selected_weight_unit = weight_unit_selector.get()
    if selected_weight_unit == "kg":
        Label3.configure(text="Weight (kg)")
        Textbox3.configure(placeholder_text="Enter your weight in kg")
    else: # "lbs"
        Label3.configure(text="Weight (lbs)")
        Textbox3.configure(placeholder_text="Enter your weight in lbs")
    
    # Clear validation labels when units change for now
    vlabel2.configure(text="")
    vlabel3.configure(text="")

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
Label1 = CTkLabel(App, text='Age', text_color=COLOR_PRIMARY_GOLD, font=FONT) # Age label unchanged
Label1.place(relx=0.05, rely=0.15, anchor=NW)

Textbox1 = CTkEntry( # Age Textbox unchanged
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    placeholder_text='Enter your age',
    placeholder_text_color=COLOR_PLACEHOLDER_LIGHT_GOLD,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8
)
Textbox1.place(relx=0.3, rely=0.20, anchor=CENTER)
Textbox1.bind("<KeyRelease>", validate_age)

vlabel1 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG) # Age validation label
vlabel1.place(relx=0.3, rely=0.123, anchor=CENTER)


# --- Height UI Elements ---
Label2 = CTkLabel(App, text='Height', text_color=COLOR_PRIMARY_GOLD, font=FONT) # Text will be updated by callback
Label2.place(relx=0.05, rely=0.30, anchor=NW)

height_unit_selector = CTkSegmentedButton(
    App, values=["cm", "ft/in"], command=update_units_ui,
    font=FONT, height=25, width=100, # Adjusted width
    selected_color=COLOR_PRIMARY_GOLD, selected_hover_color=COLOR_GOLD_HOVER,
    unselected_color=COLOR_PRIMARY_RED, unselected_hover_color=COLOR_RED_HOVER,
    text_color=COLOR_LIGHT_ACCENT, text_color_disabled=COLOR_PLACEHOLDER_LIGHT_GOLD,
    fg_color=COLOR_DARK_ACCENT,
)
height_unit_selector.set("cm") # Default to metric
height_unit_selector.place(relx=0.23, rely=0.30, anchor=NW) # Placed next to Label2

Textbox2 = CTkEntry( # Metric Height (cm)
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    text_color=COLOR_LIGHT_ACCENT, font=FONT, corner_radius=8
)
Textbox2.bind("<KeyRelease>", validate_height)

Textbox2_ft = CTkEntry( # Imperial Height (feet)
    App, width=95, height=25, # Shorter width for ft
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    text_color=COLOR_LIGHT_ACCENT, font=FONT, corner_radius=8
)
Textbox2_ft.bind("<KeyRelease>", validate_height) # Add binding

Textbox2_in = CTkEntry( # Imperial Height (inches)
    App, width=95, height=25, # Shorter width for in
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    text_color=COLOR_LIGHT_ACCENT, font=FONT, corner_radius=8
)
Textbox2_in.bind("<KeyRelease>", validate_height) # Add binding

vlabel2 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG) # Height validation label
# vlabel2 position is handled by update_units_ui initially and on change


# --- Weight UI Elements ---
Label3 = CTkLabel(App, text='Weight', text_color=COLOR_PRIMARY_GOLD, font=FONT) # Text will be updated by callback
Label3.place(relx=0.05, rely=0.45, anchor=NW)

weight_unit_selector = CTkSegmentedButton(
    App, values=["kg", "lbs"], command=update_units_ui,
    font=FONT, height=25, width=100, # Adjusted width
    selected_color=COLOR_PRIMARY_GOLD, selected_hover_color=COLOR_GOLD_HOVER,
    unselected_color=COLOR_PRIMARY_RED, unselected_hover_color=COLOR_RED_HOVER,
    text_color=COLOR_LIGHT_ACCENT, text_color_disabled=COLOR_PLACEHOLDER_LIGHT_GOLD,
    fg_color=COLOR_DARK_ACCENT
)
weight_unit_selector.set("kg") # Default to metric
weight_unit_selector.place(relx=0.23, rely=0.45, anchor=NW) # Placed next to Label3

Textbox3 = CTkEntry( # Weight (kg or lbs)
    App, width=200, height=25,
    fg_color=COLOR_PRIMARY_RED, border_color=COLOR_PRIMARY_GOLD,
    text_color=COLOR_LIGHT_ACCENT, font=FONT, corner_radius=8
)
Textbox3.place(relx=0.3, rely=0.50, anchor=CENTER) # This position might need adjustment if selectors take up more vertical space
Textbox3.bind("<KeyRelease>", validate_weight)

vlabel3 = CTkLabel(App, text='', font=FONT, text_color=COLOR_APP_BG) # Weight validation label
vlabel3.place(relx=0.3, rely=0.423, anchor=CENTER) # Original position, may need update_units_ui adjustment if Textbox3 moves.

# Call initially to set UI elements based on default "cm" and "kg"
update_units_ui()


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
Button.place(relx=0.22, rely=0.8, anchor=CENTER) # Adjusted relx to make space for Save button

# Save Record Button
SaveButton = CTkButton(
    master=App,
    text='Save Record',
    fg_color=COLOR_SUCCESS_GREEN, # Using a different color for save
    hover_color="#27AE60",        # Darker green on hover
    text_color=COLOR_LIGHT_ACCENT, # Keep text color consistent
    font=FONT,
    corner_radius=8,
    border_width=0,
    command=save_record_to_history,
    state="disabled" # Initially disabled
)
SaveButton.place(relx=0.38, rely=0.8, anchor=CENTER) # Placed next to Calculate BMI button

# View History Button
ViewHistoryButton = CTkButton(
    master=App,
    text='View History',
    fg_color=COLOR_DARK_ACCENT, # A different color for this action
    hover_color=COLOR_PRIMARY_RED,
    text_color=COLOR_LIGHT_ACCENT,
    font=FONT,
    corner_radius=8,
    border_width=0,
    command=lambda: display_history_window(App) # Pass App as master
)
ViewHistoryButton.place(relx=0.54, rely=0.8, anchor=CENTER) # Placed next to Save Record button

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