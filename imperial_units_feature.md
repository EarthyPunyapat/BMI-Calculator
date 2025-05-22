# Feature: Imperial Units Support for BMI Calculator

## Overview

This feature will enhance the existing BMI calculator by adding support for imperial units (feet, inches, and pounds). Currently, the calculator only accepts metric units (centimeters and kilograms). By incorporating imperial units, we can make the calculator more accessible and user-friendly for individuals who are more familiar with this system of measurement, particularly users in regions like the United States.

## Benefits

*   **Improved User Experience:** Users who primarily use imperial units will no longer need to manually convert their measurements to metric before using the calculator. This reduces friction and makes the tool more intuitive.
*   **Wider Applicability:** Supporting both metric and imperial units broadens the potential user base of the calculator.
*   **Increased Accuracy:** By allowing direct input in familiar units, we can reduce the chances of manual conversion errors by users.

## Proposed Changes

### User Interface (UI) Changes

1.  **Unit Selection Mechanism:**
    *   Introduce a toggle switch or a set of radio buttons (e.g., labeled "Metric" and "Imperial") allowing users to select their preferred unit system.
    *   This selector should be prominently displayed, perhaps near the height and weight input fields.

2.  **Dynamic Input Field Labels:**
    *   The labels for height and weight input fields should dynamically update based on the selected unit system.
        *   If "Metric" is selected:
            *   Height label: "Height (cm)"
            *   Weight label: "Weight (kg)"
        *   If "Imperial" is selected:
            *   Height: Instead of a single "Height" field, we'll need two input fields:
                *   "Height (ft)" for feet
                *   "Height (in)" for inches
            *   Weight label: "Weight (lbs)"

3.  **Placeholder Text Updates:**
    *   The placeholder text within the input fields should also dynamically change to reflect the selected unit system (e.g., "Enter height in ft" and "Enter height in inches").

4.  **Validation Message Updates:**
    *   Validation messages should also reflect the selected unit system. For example, if imperial is selected, height validation should check for reasonable values in feet and inches, and weight in pounds.

5.  **Report Output:**
    *   The final BMI report should clearly state the units used for the input height and weight. For example:
        *   `Height: 5 ft 10 in (178 cm)`
        *   `Weight: 160 lbs (72.5 kg)`
    *   This provides clarity and allows users to see the metric equivalents if they wish.

### Logic Changes

1.  **Unit Conversion Functions:**
    *   Implement functions to convert imperial units to metric units:
        *   `feet_inches_to_cm(feet, inches)`: Converts height from feet and inches to centimeters. (1 foot = 30.48 cm, 1 inch = 2.54 cm)
        *   `pounds_to_kg(pounds)`: Converts weight from pounds to kilograms. (1 lb = 0.453592 kg)

2.  **Input Processing:**
    *   Modify the `calculate_bmi` function (and potentially the validation functions) to:
        *   Check the selected unit system.
        *   If "Imperial" is selected:
            *   Retrieve height values from the new "feet" and "inches" input fields.
            *   Retrieve weight value from the "pounds" input field.
            *   Call the conversion functions to get height in centimeters and weight in kilograms.
        *   If "Metric" is selected, the logic remains as is (retrieve cm and kg directly).

3.  **Validation Logic Adaptation:**
    *   The `validate_height` and `validate_weight` functions need to be adapted:
        *   They should first check the selected unit system.
        *   If "Imperial" is selected:
            *   `validate_height`: Will need to validate two fields (feet and inches). Implement appropriate range checks (e.g., feet: 1-9, inches: 0-11).
            *   `validate_weight`: Implement appropriate range checks for pounds (e.g., 60-660 lbs, corresponding to approx 27-300 kg).
        *   The validation messages displayed by `vlabel2` and `vlabel3` must be updated to show imperial units and their respective valid ranges.

4.  **Core BMI Calculation:**
    *   The core BMI calculation formula (`bmi = w_kg / (h_m * h_m)`) remains unchanged, as it will always operate on metric values (kilograms and meters) after the necessary conversions are performed.

5.  **State Management:**
    *   The application needs to manage the state of the selected unit system. This state will be used by UI elements (to display correct labels/placeholders) and by the logic (to perform correct validations and conversions).

## Example Workflow (Imperial Units)

1.  User opens the BMI Calculator.
2.  User selects "Imperial" from the unit system toggle.
3.  Input field labels change:
    *   Height fields: "Height (ft)", "Height (in)"
    *   Weight field: "Weight (lbs)"
4.  User enters:
    *   Age: 30
    *   Height: 5 (ft), 10 (in)
    *   Weight: 165 (lbs)
    *   Gender: Male
    *   Pregnant: (not applicable/unchecked)
5.  User clicks "Calculate BMI".
6.  **Behind the scenes:**
    *   Validation functions check if 5 ft 10 in and 165 lbs are within valid ranges for imperial units.
    *   `feet_inches_to_cm(5, 10)` converts height to approximately 177.8 cm.
    *   `pounds_to_kg(165)` converts weight to approximately 74.84 kg.
    *   BMI is calculated using these metric values.
7.  The output report displays:
    ```
    Age: 30 years
    Gender: Male
    Height: 5 ft 10 in (177.8 cm)
    Weight: 165 lbs (74.84 kg)
    BMI : 23.6 (Normal weight)
    ```

This comprehensive approach will ensure that the "Imperial Units Support" feature is well-integrated and enhances the usability of the BMI calculator significantly.
