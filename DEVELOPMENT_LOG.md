## 📅 Development Progress

### ✅ Day 1 Progress Log

**References used:**
- [CTkinter reference video](https://www.youtube.com/watch?v=Miydkti_QVE)
- [Input validation in Tkinter](https://www.pythonguis.com/tutorials/input-validation-tkinter/)
- [CTkMessagebox library](https://github.com/Akascape/CTkMessagebox)
- [Events and Binds in Tkinter](https://python-course.eu/tkinter/events-and-binds-in-tkinter.php)

---

### 🎨 First UI Design

✅ **Problems:** Pregnant checkbox is always displayed regardless of gender selection.  
![UI Screenshot](https://github.com/user-attachments/assets/2feb043b-74f1-42f8-9073-c37836f11d5d)

🎯 **Goal:** Ensure the checkbox only appears when `Female` is selected, and disappears when another gender is chosen.

---

### ✅ Achievements:
![UI Screenshot](https://github.com/user-attachments/assets/fb2f3ff2-d5a5-489c-964d-ced0283c957b)
![UI Screenshot](https://github.com/user-attachments/assets/9952e118-a4d4-48ee-b5ce-cf1ad17be498)
- Developed a **UI prototype**
- Built **initial logic** for hiding/showing the Pregnant checkbox
- Implemented **input validation** for:
  - Age
  - Height
  - Weight

---

## 📅 Day 2 Progress Log

### ✅ New Features / Changes:
- Switched from using a messagebox to an **output textbox (report box)** displayed on the right side of the UI
- Implemented **BMI calculation function** with category interpretation
- Added **validation for Calculate button** → shows an error message inside the output box if any input is invalid
- Added logic to **prevent BMI calculation if pregnant** (shows message in output box)
- Improved UI styling → **Iron Man themed color palette**
- Implemented **input restriction: entries now only accept numbers**
- Removed the old function that showed/hid the checkbox when selecting "Female" (checkbox always visible now)
- 
![Image](https://github.com/user-attachments/assets/8ab4a200-43cb-4d8f-80c9-895d0cb9629d)

---

### ⚠️ Problems and solutions:
| Problem | Solution |
|---------|----------|
| Messagebox didn’t work well for displaying multi-line output | Switched to using a **textbox output area instead** |
| Attempt to merge validation functions made code harder to debug | Kept **separate validation functions** |

---
