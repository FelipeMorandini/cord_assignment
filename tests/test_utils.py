import os
import json
import unittest
import pandas as pd
from unittest.mock import patch
from src.utils import export_to_excel, load_json_data, time_to_minutes, format_time, find_stop_name_by_id, compare_times, calculate_breaks

class TestLoadJsonData(unittest.TestCase):

    def test_load_valid_file(self):
        test_data = {'key1': 'value1'}
        with open('./tests/test.json', 'w') as f:
            json.dump(test_data, f)
        
        result = load_json_data('./tests/test.json')
        self.assertEqual(result, test_data)

    def test_load_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            load_json_data('./tests/invalid.json')

    def test_load_invalid_json(self):
        with open('./tests/invalid.json', 'w') as f:
            f.write('invalid')
        
        with self.assertRaises(json.JSONDecodeError):
            load_json_data('./tests/invalid.json')

class TestTimeToMinutes(unittest.TestCase):

    def test_normal(self):
        time_str = '1.8:30'
        expected = 1260
        actual = time_to_minutes(time_str)
        self.assertEqual(actual, expected)

    def test_cross_day_boundary(self):
        time_str = '2.3:45' 
        expected = 2865
        actual = time_to_minutes(time_str)
        self.assertEqual(actual, expected)

    def test_invalid_format(self):
        time_str = 'invalid'
        with self.assertRaises(ValueError):
            time_to_minutes(time_str)

    def test_missing_day(self):
        time_str = '3:15'
        with self.assertRaises(ValueError):
            time_to_minutes(time_str)

    def test_negative_day(self):
        time_str = '-1.2:30'
        with self.assertRaises(ValueError):
            time_to_minutes(time_str)

    def test_invalid_hours(self):
        time_str = '1.25:30'
        with self.assertRaises(ValueError):
            time_to_minutes(time_str)

    def test_invalid_minutes(self):
        time_str = '1.2:60'
        with self.assertRaises(ValueError):
            time_to_minutes(time_str)

class TestFormatTime(unittest.TestCase):

    def test_normal(self):
        minutes = 180
        expected = '0.03:00'
        actual = format_time(minutes)
        self.assertEqual(actual, expected)

    def test_cross_day_boundary(self):
        minutes = 1440
        expected = '1.00:00'
        actual = format_time(minutes) 
        self.assertEqual(actual, expected)

    def test_zero_minutes(self):
        minutes = 0
        expected = '0.00:00'
        actual = format_time(minutes)
        self.assertEqual(actual, expected)

    def test_negative_minutes(self):
        minutes = -15
        with self.assertRaises(ValueError):
            format_time(minutes)

    def test_string_input(self):
        minutes = 'string'
        with self.assertRaises(TypeError):
            format_time(minutes)

class TestFindStopNameById(unittest.TestCase):

    def test_find_existing_stop(self):
        stops = [{'stop_id': 1, 'stop_name': 'Stop 1'}, 
                 {'stop_id': 2, 'stop_name': 'Stop 2'}]
        stop_id = 1
        expected = 'Stop 1'
        actual = find_stop_name_by_id(stop_id, stops)
        self.assertEqual(actual, expected)

    def test_find_non_existing_stop(self):
        stops = [{'stop_id': 1, 'stop_name': 'Stop 1'}, 
                 {'stop_id': 2, 'stop_name': 'Stop 2'}]
        stop_id = 3
        expected = 'Unknown Stop'
        actual = find_stop_name_by_id(stop_id, stops)
        self.assertEqual(actual, expected)

    def test_empty_stops_list(self):
        stops = []
        stop_id = 1
        expected = 'Unknown Stop'
        actual = find_stop_name_by_id(stop_id, stops)
        self.assertEqual(actual, expected)
        
class TestCompareTimes(unittest.TestCase):

    def test_time1_less_than_time2(self):
        time1 = '1.2:30'
        time2 = '1.3:45'
        self.assertTrue(compare_times(time1, time2))
    
    def test_time1_greater_than_time2(self):
        time1 = '1.3:45'
        time2 = '1.2:30'
        self.assertFalse(compare_times(time1, time2))
    
    def test_equal_times(self):
        time1 = '1.2:30'
        time2 = '1.2:30'
        self.assertFalse(compare_times(time1, time2))
    
    def test_cross_day_boundary(self):
        time1 = '1.23:45'
        time2 = '2.1:15'
        self.assertTrue(compare_times(time1, time2))

class TestCalculateBreaks(unittest.TestCase):

    def test_no_breaks(self):
        vehicle_events = [
            {'start_time': '1.00:00', 'end_time': '1.30:00', 'destination_stop_id': 'A'},
            {'start_time': '1.35:00', 'end_time': '2.00:00', 'destination_stop_id': 'B'}
        ]
        stops = [{'stop_id': 'A', 'stop_name': 'Stop A'}, {'stop_id': 'B', 'stop_name': 'Stop B'}]
        breaks = calculate_breaks(vehicle_events, stops)
        self.assertEqual(breaks, [])

    def test_one_break(self):
        vehicle_events = [
            {'start_time': '1.00:00', 'end_time': '1.30:00', 'destination_stop_id': 'A'}, 
            {'start_time': '1.45:00', 'end_time': '2.00:00', 'destination_stop_id': 'B'}
        ]
        stops = [{'stop_id': 'A', 'stop_name': 'Stop A'}, {'stop_id': 'B', 'stop_name': 'Stop B'}]
        breaks = calculate_breaks(vehicle_events, stops)
        expected = [{'break_start_time': '1.30:00', 'break_duration': 15, 'break_stop_name': 'Stop A'}]
        self.assertEqual(breaks, expected)

    def test_multiple_breaks(self):
        vehicle_events = [
            {'start_time': '1.00:00', 'end_time': '1.30:00', 'destination_stop_id': 'A'},
            {'start_time': '1.45:00', 'end_time': '2.00:00', 'destination_stop_id': 'B'},
            {'start_time': '2.30:00', 'end_time': '3.00:00', 'destination_stop_id': 'C'}
        ]
        stops = [{'stop_id': 'A', 'stop_name': 'Stop A'}, {'stop_id': 'B', 'stop_name': 'Stop B'}, {'stop_id': 'C', 'stop_name': 'Stop C'}]
        breaks = calculate_breaks(vehicle_events, stops)
        expected = [
            {'break_start_time': '1.30:00', 'break_duration': 15, 'break_stop_name': 'Stop A'},
            {'break_start_time': '2.00:00', 'break_duration': 30, 'break_stop_name': 'Stop B'}
        ]
        self.assertEqual(breaks, expected)
        
class TestExportToExcel(unittest.TestCase):

    def test_step_1(self):
        data = [{'Duty ID': 1, 'Start Time': '8:00', 'End Time': '12:00'}]
        export_to_excel(data, './tests/test', 1)
        # Assert file was created
        self.assertTrue(os.path.exists('./tests/test.xlsx'))  

    def test_step_2(self):
        data = [{'Duty ID': 1, 'Start Time': '8:00', 'End Time': '12:00', 'First Stop': 'Stop 1', 'Last Stop': 'Stop 2'}]
        export_to_excel(data, 'test', 2)
        # Assert file was created with correct columns
        df = pd.read_excel('./tests/test.xlsx')
        self.assertEqual(list(df.columns), ['Duty ID', 'Start Time', 'End Time', 'First Stop', 'Last Stop'])

    def test_step_3(self):
        data = [{'Duty ID': 1, 'Start Time': '8:00', 'End Time': '12:00', 'First Stop': 'Stop 1', 'Last Stop': 'Stop 2', 'Breaks': [{'break_start_time': '10:00', 'break_duration': 30, 'break_stop_name': 'Stop 3'}]}]
        export_to_excel(data, 'test', 3)
        # Assert file was created with correct columns including break info
        df = pd.read_excel('./tests/test.xlsx')
        expected_columns = ['Duty ID', 'Start Time', 'End Time', 'First Stop', 'Last Stop', 'Break Start Time', 'Break Duration', 'Break Stop Name']
        self.assertEqual(list(df.columns), expected_columns)

    def test_invalid_step(self):
        data = []
        export_to_excel(data, './tests/test', 4)
        # Assert error message is printed
        self.assertRaises(SystemExit, export_to_excel, data, 'test', 4)

    def test_file_write_error(self):
        # Mock error when writing file
        with patch('pandas.DataFrame.to_excel', side_effect=Exception('Test error')):
            data = []
            export_to_excel(data, './tests/test', 1)
            # Assert error message is printed
            self.assertRaises(Exception, export_to_excel, data, 'test', 1)