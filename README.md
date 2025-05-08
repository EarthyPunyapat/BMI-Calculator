
# Tkinter GUI Project

## 📅 Day 1 Progress Log

**References used:**
- [CTkinter reference video](https://www.youtube.com/watch?v=Miydkti_QVE)
- [Input validation in Tkinter](https://www.pythonguis.com/tutorials/input-validation-tkinter/)
- [CTkMessagebox library](https://github.com/Akascape/CTkMessagebox)
- [Events and Binds in Tkinter](https://python-course.eu/tkinter/events-and-binds-in-tkinter.php)

---

## 🎨 First UI Design

✅ **Problems:** Pregnant checkbox is always displayed regardless of gender selection.  
![Image](https://github.com/user-attachments/assets/2feb043b-74f1-42f8-9073-c37836f11d5d)

🎯 **Goal:** Ensure the checkbox only appears when `Female` is selected, and disappears when another gender is chosen.

---

## ✅ **Things Done Today:**
![Image](https://github.com/user-attachments/assets/fb2f3ff2-d5a5-489c-964d-ced0283c957b)
![Image](https://github.com/user-attachments/assets/9952e118-a4d4-48ee-b5ce-cf1ad17be498)
- Developed a **UI prototype**
- Built **half-completed logic** for hiding/showing the Pregnant checkbox
- Implemented **input validation** for:
  - Age
  - Height
  - Weight

---

## 🚀 Planned Improvements:
- ✅ Complete conditional visibility for the Pregnant checkbox
- ✅ Add more input validation (e.g., range checks for valid age, weight, height)
- ✅ Implement BMI calculation formula
- ✅ Display BMI result with interpretation (underweight, normal, overweight, obesity)
- ✅ Alert if BMI is unsuitable (e.g., pregnant, invalid ranges)
- ✅ Generate and display BMI report onscreen
- ✅ Save BMI report to a file (for printing/emailing)
- ✅ Ensure input fields only accept integers
- ✅ Add looping/iteration for input checking
- ✅ Use iteration for report header formatting (e.g., asterisks)

---

## 🛠️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BMI-Calculator.git
   cd BMI-Calculator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python main.py
   ```

---

## 💡 Libraries Used
- `customtkinter`
- `CTkMessagebox`

