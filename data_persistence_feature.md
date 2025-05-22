# Feature: Data Persistence (BMI History Tracking)

## Overview

This feature introduces "Data Persistence" to the BMI calculator, allowing users to save their BMI calculation results and view them later. Currently, each BMI calculation is ephemeral; once the application is closed or a new calculation is made, the previous result is lost. With data persistence, users can maintain a history of their BMI records, enabling them to track their progress and observe trends over time.

## Benefits

*   **Progress Tracking:** Users can monitor changes in their BMI, weight, and BMI category over weeks, months, or years. This is particularly useful for individuals actively working towards weight management goals.
*   **Historical Overview:** Provides a convenient way to look back at past measurements without needing to remember or manually log them elsewhere.
*   **Increased Engagement:** The ability to save and review data can make the tool more engaging and valuable for long-term use.
*   **Data-Driven Insights:** Users can potentially identify patterns or see the impact of lifestyle changes on their BMI over time.

## Proposed Changes

### User Interface (UI) Changes

1.  **Save Record Button:**
    *   After a BMI calculation is successfully performed and the report is displayed, a "Save Record" or "Log this BMI" button should become active.
    *   Clicking this button would save the current calculation's data (Date, Age, Height, Weight, BMI, Category).

2.  **History View/Section:**
    *   A new section or tab within the application titled "BMI History" or "My Progress".
    *   This area would display a list or table of saved BMI records.
    *   Each record in the history view should ideally show:
        *   Date of calculation
        *   Age (at the time of calculation)
        *   Weight (with units, e.g., kg or lbs)
        *   Height (with units, e.g., cm or ft/in)
        *   Calculated BMI value
        *   BMI Category (e.g., "Normal weight")
    *   The table should be scrollable if the number of records is large.

3.  **Controls for History:**
    *   **Load History:** While history might load automatically on startup, a button to "View History" or "Refresh History" could be useful.
    *   **Delete Record(s):** Functionality to delete individual records or perhaps an option to "Clear All History" (with a confirmation dialog).
    *   **Sort Options (Optional):** Ability to sort the history table by date (ascending/descending) would be a nice enhancement.

4.  **Visual Cues:**
    *   A confirmation message (e.g., "Record saved!" or "History cleared.") after performing data operations.

### Logic Changes

1.  **Data Storage Mechanism:**
    *   Choose a method for local data storage. Options include:
        *   **CSV File:** Simple to implement, human-readable. Each row represents a BMI record.
        *   **JSON File:** Structured, good for web-based applications, but also viable for local apps. Each record could be a JSON object within a list.
        *   **SQLite Database:** A lightweight, file-based SQL database. More robust for querying, sorting, and managing larger datasets, but adds a dependency (though `sqlite3` is standard in Python).
    *   For simplicity in a CustomTkinter app, a **CSV or JSON file** is likely sufficient and easier to manage initially. Let's assume CSV for this description.
    *   The data file would store: `timestamp, age, height_cm, weight_kg, bmi_value, bmi_category, (optionally: height_imperial_ft, height_imperial_in, weight_imperial_lbs if imperial support is also added)`.

2.  **Saving Data:**
    *   When the "Save Record" button is clicked:
        *   The application will gather the current data: current date/time, age, height (in a consistent unit, e.g., cm), weight (in a consistent unit, e.g., kg), calculated BMI, and BMI category.
        *   This data will be appended as a new entry (e.g., a new row in a CSV file) to the storage file.
        *   Handle file creation if it doesn't exist.

3.  **Loading Data:**
    *   On application startup, or when the user navigates to the "BMI History" view:
        *   The application will check for the existence of the data file.
        *   If it exists, read its contents (e.g., parse the CSV rows or JSON objects).
        *   Populate the history view (table/list) with the loaded records.
        *   Handle cases where the file is empty or corrupted (e.g., display "No history yet." or an error message).

4.  **Deleting Data:**
    *   **Delete Single Record:**
        *   The user selects a record in the history view.
        *   Clicks a "Delete Selected" button.
        *   The application identifies the record in its internal representation of the history and removes it.
        *   The data storage file is then overwritten with the updated history (or the specific record is removed if the storage format allows, though rewriting is often simpler for CSV/JSON).
    *   **Clear All History:**
        *   User clicks "Clear All History".
        *   After confirmation, the application deletes the data file or clears its contents.
        *   The history view is updated to show it's empty.

5.  **Data Integrity and Error Handling:**
    *   Implement basic error handling for file operations (e.g., unable to read/write the file).
    *   Ensure data is saved and loaded in a consistent format.

6.  **Interaction with Other Features:**
    *   If "Imperial Units Support" is implemented, decide how to store height/weight:
        *   Option 1: Always convert to metric before saving to maintain consistency in the data file. The display can convert back if needed or show both.
        *   Option 2: Store the originally entered units as well, adding more columns to the data file. This might be better for display accuracy in the history.
    *   The date/timestamp of the record is crucial for tracking.

## Example Workflow

1.  User calculates their BMI. The report shows: Age 30, Height 170cm, Weight 70kg, BMI 24.2 (Normal weight).
2.  User clicks "Save Record".
3.  A new entry is added to `bmi_history.csv`: `YYYY-MM-DD HH:MM:SS,30,170,70,24.2,Normal weight`.
4.  Later, the user opens the app and navigates to the "BMI History" tab.
5.  The app reads `bmi_history.csv` and displays a table with all saved records, including the one above.
6.  User selects an old record and clicks "Delete Record". The record is removed from the table and the `bmi_history.csv` file is updated.

This feature would transform the BMI calculator from a simple one-off tool into a personal health companion for tracking an important health metric.
