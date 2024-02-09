# import unittest
# from src.steps import generate_start_end_times

# class TestGenerateStartEndTimes(unittest.TestCase):

#     def test_normal(self):
#         duties = [{'duty_id': 1}, {'duty_id': 2}]
#         vehicles = [{'vehicle_events': [{'duty_id': 1, 'start_time': '8:00', 'end_time': '10:00'}, {'duty_id': 1, 'start_time': '7:00', 'end_time': '11:00'}]}, 
#                     {'vehicle_events': [{'duty_id': 2, 'start_time': '9:00', 'end_time': '14:00'}]}]
#         expected = [{'Duty ID': 1, 'Start Time': '7:00', 'End Time': '11:00'}, 
#                     {'Duty ID': 2, 'Start Time': '9:00', 'End Time': '14:00'}]
#         actual = generate_start_end_times(duties, vehicles)
#         self.assertEqual(actual, expected)

#     def test_no_start_time(self):
#         duties = [{'duty_id': 1}]
#         vehicles = [{'vehicle_events': [{'duty_id': 1, 'end_time': '10:00'}]}]
#         expected = [{'Duty ID': 1, 'Start Time': 'No Start Time Found', 'End Time': '10:00'}]
#         actual = generate_start_end_times(duties, vehicles)
#         self.assertEqual(actual, expected)

#     def test_no_end_time(self):
#         duties = [{'duty_id': 1}]
#         vehicles = [{'vehicle_events': [{'duty_id': 1, 'start_time': '8:00'}]}]
#         expected = [{'Duty ID': 1, 'Start Time': '8:00', 'End Time': 'No End Time Found'}]
#         actual = generate_start_end_times(duties, vehicles)
#         self.assertEqual(actual, expected)

#     def test_no_matching_events(self):
#         duties = [{'duty_id': 1}]
#         vehicles = [{'vehicle_events': []}]
#         expected = [{'Duty ID': 1, 'Start Time': 'No Start Time Found', 'End Time': 'No End Time Found'}]
#         actual = generate_start_end_times(duties, vehicles)
#         self.assertEqual(actual, expected)