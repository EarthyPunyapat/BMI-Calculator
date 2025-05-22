# Tkinter BMI Calculator Project

## 🎯 Project Overview

A BMI calculator built using **CustomTkinter** for doctors and nurses to easily input patient details (age, gender, height, weight), validate input, and generate a BMI report onscreen. The program prevents BMI calculation for pregnant patients and ensures user-friendly validation and feedback.

---

## Features
- Accurate BMI calculation based on age, height, weight, and gender.
- Input validation for age, height, and weight with user-friendly error messages.
- Option to specify gender (Male/Female).
- Special consideration for pregnancy (BMI calculation disabled for pregnant females).
- Clear display of input values and calculated BMI report.
- Themed user interface using CustomTkinter.

## Technologies Used
- Python
- CustomTkinter library for the graphical user interface.

## How to Use
1. Enter your age in years (must be between 18 and 79).
2. Enter your height in centimeters (must be between 45 and 270).
3. Enter your weight in kilograms (must be between 30 and 300).
4. Select your gender from the dropdown menu.
5. If female, indicate if pregnant using the checkbox.
6. Click the "Calculate BMI" button.
7. Your BMI and a brief report will be displayed in the output area on the right.
8. If there are any input errors, messages will guide you to correct them.

---

## Screenshots
*(Coming Soon: Add screenshots of the application interface here.)*

## 🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5. Push to the branch (`git push origin feature/AmazingFeature`).
6. Open a Pull Request.

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🛠️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EarthyPunyapat/BMI-Calculator.git
   cd BMI-Calculator
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Mac/Linux
   .venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install customtkinter
   pip install CTkMessagebox
   ```

4. **Run the program:**
   ```bash
   python BMI-Cal.py
   ```
