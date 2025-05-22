import unittest
import sys
import os
import json
import datetime

# ----- Conversion Functions (copied from BMI_Cal.py) -----
def feet_inches_to_cm(feet_str, inches_str):
    try:
        feet = float(feet_str)
        inches = float(inches_str)
        if feet < 0 or inches < 0:
            return None
        return (feet * 30.48) + (inches * 2.54)
    except ValueError:
        return None

def pounds_to_kg(pounds_str):
    try:
        pounds = float(pounds_str)
        if pounds < 0:
            return None
        return pounds * 0.45359237
    except ValueError:
        return None

# ----- BMI Core Calculation Logic (copied from BMI_Cal.py) -----
def _calculate_bmi_core(h_cm, w_kg):
    if h_cm <= 0 or w_kg <= 0:
        return 0.0
    h_m = h_cm / 100
    bmi = w_kg / (h_m * h_m)
    return bmi

# ----- Age-Specific BMI Category Logic (copied from BMI_Cal.py) -----
def _get_age_specific_bmi_category(bmi_value, age):
    category = "Not determined"
    if 18 <= age <= 24:
        if bmi_value < 18.5: category = "Underweight"
        elif bmi_value < 23: category = "Normal weight (18-24 yrs)"
        elif bmi_value < 28: category = "Overweight (18-24 yrs)"
        else: category = "Obese (18-24 yrs)"
    elif 25 <= age <= 64:
        if bmi_value < 18.5: category = "Underweight"
        elif bmi_value < 25: category = "Normal weight (25-64 yrs)"
        elif bmi_value < 30: category = "Overweight (25-64 yrs)"
        else: category = "Obese (25-64 yrs)"
    elif age >= 65:
        if bmi_value < 22: category = "Underweight (65+ yrs)"
        elif bmi_value < 27: category = "Normal weight (65+ yrs)"
        elif bmi_value < 30: category = "Overweight (65+ yrs)"
        else: category = "Obese (65+ yrs)"
    return category

# ----- Data Persistence Logic (adapted for testing) -----
TEST_BMI_HISTORY_FILE = "test_bmi_history.json"

# Mock App and Output objects for testing save_record_to_history
class MockApp:
    def __init__(self):
        self.current_bmi_details = None

class MockOutput:
    def __init__(self):
        self.text_content = ""
        self.state_log = [] # To track state changes if needed
    def configure(self, state):
        self.state_log.append(state)
    def delete(self, start, end):
        self.text_content = "" 
    def insert(self, position, text):
        if position == "end":
            self.text_content += text
        elif position == "0.0": # As used in save_record_to_history for error messages
            self.text_content = text
        else: # Fallback for other uses, though not expected by current save_record_to_history
            self.text_content = text 
    def get(self, start, end): # As used by save_record_to_history
        return self.text_content 

# These global mocks will be used by the copied save_record_to_history
App = MockApp()
Output = MockOutput()

def load_records_from_history_test(): 
    try:
        with open(TEST_BMI_HISTORY_FILE, 'r') as f:
            records = json.load(f)
        return records
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception: 
        return []

def save_record_to_history_test(): 
    global App, Output # Ensure we're using the test globals
    if not hasattr(App, 'current_bmi_details') or App.current_bmi_details is None:
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "No BMI data to save. Please calculate BMI first.")
        Output.configure(state='disabled')
        return False 

    new_record = App.current_bmi_details
    required_fields = ["date", "age", "gender", "height_str", "weight_str", "bmi_value", "bmi_category"]
    if not all(field in new_record for field in required_fields):
        Output.configure(state='normal')
        Output.delete("0.0", "end")
        Output.insert("0.0", "Error: Incomplete BMI data for saving.")
        Output.configure(state='disabled')
        return False

    records = load_records_from_history_test()
    records.append(new_record)

    try:
        with open(TEST_BMI_HISTORY_FILE, 'w') as f:
            json.dump(records, f, indent=4)
        # Simulate the original Output.get() before appending success message
        # current_output_content = Output.get("0.0", "end").strip() 
        # Output.delete("0.0", "end")
        # Output.insert("0.0", current_output_content) # Restore original
        Output.insert("end", "\n\n--- Record Saved Successfully! ---") # Append success
        return True
    except Exception as e:
        Output.insert("end", f"\n\n--- Error saving record: {e} ---") 
        return False


class TestConversionFunctions(unittest.TestCase):
    def test_feet_inches_to_cm_valid(self):
        self.assertAlmostEqual(feet_inches_to_cm("5", "10"), 177.8, places=1)
        self.assertAlmostEqual(feet_inches_to_cm("6", "0"), 182.88, places=2)
        self.assertAlmostEqual(feet_inches_to_cm("5", "0"), 152.4, places=1)
        self.assertAlmostEqual(feet_inches_to_cm("0", "6"), 15.24, places=2)
        self.assertAlmostEqual(feet_inches_to_cm("4", "11.5"), 151.13, places=2)
        self.assertAlmostEqual(feet_inches_to_cm("5.5", "0"), 167.64, places=2)

    def test_feet_inches_to_cm_invalid(self):
        self.assertIsNone(feet_inches_to_cm("abc", "10"))
        self.assertIsNone(feet_inches_to_cm("5", "xyz"))
        self.assertIsNone(feet_inches_to_cm("-5", "10"))
        self.assertIsNone(feet_inches_to_cm("5", "-10"))
        self.assertIsNone(feet_inches_to_cm("", "10"))
        self.assertIsNone(feet_inches_to_cm("5", ""))

    def test_pounds_to_kg_valid(self):
        self.assertAlmostEqual(pounds_to_kg("165"), 74.84274105, places=5)
        self.assertAlmostEqual(pounds_to_kg("0"), 0.0, places=1)
        self.assertAlmostEqual(pounds_to_kg("100.5"), 45.586034685, places=5)

    def test_pounds_to_kg_invalid(self):
        self.assertIsNone(pounds_to_kg("abc"))
        self.assertIsNone(pounds_to_kg("-150"))
        self.assertIsNone(pounds_to_kg(""))

class TestBMICalculationLogic(unittest.TestCase):
    def test_bmi_normal_weight(self):
        h_cm = feet_inches_to_cm("5", "10")
        w_kg = pounds_to_kg("165")
        self.assertIsNotNone(h_cm); self.assertIsNotNone(w_kg)
        bmi = _calculate_bmi_core(h_cm, w_kg)
        self.assertAlmostEqual(bmi, 23.7, places=1)

    def test_bmi_normal_weight_metric_direct(self):
        bmi = _calculate_bmi_core(177.8, 74.8427) 
        self.assertAlmostEqual(bmi, 23.7, places=1)

    def test_bmi_underweight(self):
        h_cm = feet_inches_to_cm("5", "8")
        w_kg = pounds_to_kg("110")
        self.assertIsNotNone(h_cm); self.assertIsNotNone(w_kg)
        bmi = _calculate_bmi_core(h_cm, w_kg)
        self.assertAlmostEqual(bmi, 16.7, places=1)

    def test_bmi_overweight(self):
        h_cm = feet_inches_to_cm("5", "5")
        w_kg = pounds_to_kg("170")
        self.assertIsNotNone(h_cm); self.assertIsNotNone(w_kg)
        bmi = _calculate_bmi_core(h_cm, w_kg) 
        self.assertAlmostEqual(bmi, 28.3, places=1) 
        
    def test_bmi_obese(self):
        h_cm = feet_inches_to_cm("6", "0")
        w_kg = pounds_to_kg("250")
        self.assertIsNotNone(h_cm); self.assertIsNotNone(w_kg)
        bmi = _calculate_bmi_core(h_cm, w_kg) 
        self.assertAlmostEqual(bmi, 33.9, places=1) 

    def test_bmi_with_zero_or_negative_input_to_core(self):
        self.assertEqual(_calculate_bmi_core(0, 70), 0.0)
        self.assertEqual(_calculate_bmi_core(170, 0), 0.0)
        self.assertEqual(_calculate_bmi_core(-170, 70), 0.0)

class TestAgeSpecificBMICategories(unittest.TestCase):
    def test_age_group_18_24(self):
        self.assertEqual(_get_age_specific_bmi_category(18.4, 18), "Underweight")
        self.assertEqual(_get_age_specific_bmi_category(18.5, 20), "Normal weight (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(22.9, 24), "Normal weight (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(23.0, 18), "Overweight (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(27.9, 20), "Overweight (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(28.0, 24), "Obese (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(30.0, 20), "Obese (18-24 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(17.0, 20), "Underweight")

    def test_age_group_25_64(self):
        self.assertEqual(_get_age_specific_bmi_category(18.4, 25), "Underweight")
        self.assertEqual(_get_age_specific_bmi_category(18.5, 30), "Normal weight (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(24.9, 64), "Normal weight (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(25.0, 25), "Overweight (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(29.9, 30), "Overweight (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(30.0, 64), "Obese (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(35.0, 30), "Obese (25-64 yrs)")
        self.assertEqual(_get_age_specific_bmi_category(17.0, 30), "Underweight")

    def test_age_group_65_plus(self):
        self.assertEqual(_get_age_specific_bmi_category(21.9, 65), "Underweight (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(22.0, 70), "Normal weight (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(26.9, 99), "Normal weight (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(27.0, 65), "Overweight (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(29.9, 70), "Overweight (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(30.0, 99), "Obese (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(35.0, 70), "Obese (65+ yrs)")
        self.assertEqual(_get_age_specific_bmi_category(25.0, 99), "Normal weight (65+ yrs)")


class TestDataPersistence(unittest.TestCase):
    def setUp(self):
        global App, Output # Ensure we are modifying the global mocks
        App = MockApp()
        Output = MockOutput() 
        if os.path.exists(TEST_BMI_HISTORY_FILE):
            os.remove(TEST_BMI_HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(TEST_BMI_HISTORY_FILE):
            os.remove(TEST_BMI_HISTORY_FILE)

    def _create_sample_record(self, index=0, age_suffix=""):
        # Suffix is now just for string fields if needed, index for numeric variation
        return {
            "date": datetime.date.today().isoformat(),
            "age": f"3{index}{age_suffix}", # e.g. "30", "31_A"
            "gender": "Male",
            "height_str": f"18{index} cm",
            "weight_str": f"7{index} kg",
            "bmi_value": 23.15 + index, # Numeric variation
            "bmi_category": "Normal weight (25-64 yrs)"
        }

    def test_load_from_non_existent_file(self):
        records = load_records_from_history_test()
        self.assertEqual(records, [])

    def test_save_and_load_single_record(self):
        App.current_bmi_details = self._create_sample_record(index=0)
        self.assertTrue(save_record_to_history_test())
        
        records = load_records_from_history_test()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["age"], "30")
        self.assertEqual(records[0]["bmi_value"], 23.15)

    def test_save_and_load_multiple_records(self):
        record1 = self._create_sample_record(index=1, age_suffix="_A")
        record2 = self._create_sample_record(index=2, age_suffix="_B")

        App.current_bmi_details = record1
        self.assertTrue(save_record_to_history_test())
        
        # Reset Output mock text if necessary, or save_record_to_history_test should handle it
        Output.text_content = "" # Resetting to check next save message clearly
        App.current_bmi_details = record2 
        self.assertTrue(save_record_to_history_test())

        records = load_records_from_history_test()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["age"], "31_A")
        self.assertEqual(records[1]["age"], "32_B")
        self.assertEqual(records[0]["bmi_value"], 23.15 + 1)
        self.assertEqual(records[1]["bmi_value"], 23.15 + 2)


    def test_save_appends_to_existing_history(self):
        initial_record = self._create_sample_record(index=0, age_suffix="_initial")
        with open(TEST_BMI_HISTORY_FILE, 'w') as f:
            json.dump([initial_record], f, indent=4)

        App.current_bmi_details = self._create_sample_record(index=1, age_suffix="_new")
        self.assertTrue(save_record_to_history_test())

        records = load_records_from_history_test()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["age"], "30_initial")
        self.assertEqual(records[1]["age"], "31_new")

    def test_load_from_malformed_json(self):
        with open(TEST_BMI_HISTORY_FILE, 'w') as f:
            f.write("This is not valid JSON {")
        
        records = load_records_from_history_test()
        self.assertEqual(records, [])

    def test_save_record_no_details(self):
        App.current_bmi_details = None
        self.assertFalse(save_record_to_history_test())
        self.assertIn("No BMI data to save", Output.text_content)
        self.assertFalse(os.path.exists(TEST_BMI_HISTORY_FILE))

    def test_save_record_incomplete_details(self):
        App.current_bmi_details = {"date": "2023-01-01", "age": "25"}
        self.assertFalse(save_record_to_history_test())
        self.assertIn("Incomplete BMI data", Output.text_content)
        self.assertFalse(os.path.exists(TEST_BMI_HISTORY_FILE))

if __name__ == '__main__':
    unittest.main()
