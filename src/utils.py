import json
import pandas as pd

"""Load JSON data from a file.

Args:
    filepath (str): The path to the JSON file to load.

Returns:
    dict: The JSON data loaded from the file.
"""
def load_json_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {filepath} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"The file {filepath} contains invalid JSON.")
        return None

"""Convert time from 'day.offset.hours:minutes' format to total minutes.

Args:
  time_str (str): The time string in 'day.offset.hours:minutes' format.

Returns:
  int: The total minutes.
"""
def time_to_minutes(time_str):
    day, time = time_str.split('.')
    hours, minutes = map(int, time.split(':'))
    return int(day) * 24 * 60 + hours * 60 + minutes

"""Convert total minutes back into 'day.offset.hours:minutes' format.

Args:
  minutes (int): The number of total minutes. 

Returns:
  str: The time string in 'day.offset.hours:minutes' format.
"""
def format_time(minutes):
    days = minutes // (24 * 60)
    remaining_minutes = minutes % (24 * 60)
    hours = remaining_minutes // 60
    minutes = remaining_minutes % 60
    return f"{days}.{hours:02d}:{minutes:02d}"

"""
Return the stop name given a stop ID by searching through a list of stops.

Args:
  stop_id: The ID of the stop to search for.
  stops: The list of stops to search through.

Returns:
  The name of the stop with the given ID if found, otherwise 'Unknown Stop'.
"""
def find_stop_name_by_id(stop_id, stops):
    for stop in stops:
        if stop['stop_id'] == stop_id:
            return stop['stop_name']
    return "Unknown Stop"

"""
Compare two times in 'day.offset.hours:minutes' format.

Returns True if time1 is before time2, else False.
"""
def compare_times(time1, time2):
    return time_to_minutes(time1) < time_to_minutes(time2)


"""
Calculates all breaks longer than 15 minutes from a list of vehicle events.

Breaks are found by looking at the duration between the end time of one event 
and the start time of the next event. If the duration is over 15 minutes, it is 
considered a break. Information about each break is collected into a dictionary 
and the list of break dictionaries is returned.

Args:
  vehicle_events: List of vehicle event dicts with start_time and end_time keys. 
  stops: List of stop dicts with stop_id and stop_name keys.

Returns: 
  list: List of dicts containing info about each detected break.
"""
def calculate_breaks(vehicle_events, stops):
    breaks = []
    for i in range(len(vehicle_events) - 1):
        end_current_event = time_to_minutes(vehicle_events[i]['end_time'])
        start_next_event = time_to_minutes(vehicle_events[i + 1]['start_time'])
        duration = start_next_event - end_current_event
        if duration > 15:  # Breaks longer than 15 minutes
            break_info = {
                'break_start_time': format_time(end_current_event),
                'break_duration': duration,
                'break_stop_name': find_stop_name_by_id(vehicle_events[i]['destination_stop_id'], stops)
            }
            breaks.append(break_info)
    return breaks

"""Exports the given report data to an Excel file.

The data structure and columns exported depends on the provided 
step number:

1. Exports a simple list of dicts with Duty ID, Start Time and End Time.

2. Exports a flattened structure with duty info and first/last stops.

3. Exports duty info along with a separate row for each break.

Handles errors writing the Excel file.
"""
def export_to_excel(data, filename, step):
    """Export report data to an Excel file."""
    # Convert the data into a pandas DataFrame.
    if step == 1:
        columns = ['Duty ID', 'Start Time', 'End Time']
        df = pd.DataFrame(data, columns=columns)
    elif step == 2:
        # Flatten the data structure if necessary and create a DataFrame.
        df = pd.DataFrame(data)[['Duty ID', 'Start Time', 'End Time', 'First Stop', 'Last Stop']]
    elif step == 3:
        # For step 3, we will need to handle the nested 'Breaks' information.
        # We will create a new row for each break.
        rows = []
        for duty in data:
            for break_info in duty['Breaks']:
                row = {
                    'Duty ID': duty['Duty ID'],
                    'Start Time': duty['Start Time'],
                    'End Time': duty['End Time'],
                    'First Stop': duty['First Stop'],
                    'Last Stop': duty['Last Stop'],
                    'Break Start Time': break_info['break_start_time'],
                    'Break Duration': break_info['break_duration'],
                    'Break Stop Name': break_info['break_stop_name']
                }
                rows.append(row)
            if not duty['Breaks']:
                # If there are no breaks, still add the duty info as a row.
                rows.append({
                    'Duty ID': duty['Duty ID'],
                    'Start Time': duty['Start Time'],
                    'End Time': duty['End Time'],
                    'First Stop': duty['First Stop'],
                    'Last Stop': duty['Last Stop'],
                    'Break Start Time': None,
                    'Break Duration': None,
                    'Break Stop Name': None
                })
        df = pd.DataFrame(rows)
    
    else:
        print("Invalid step number. Please enter a number between 1 and 3.")
    
    # Write the DataFrame to an Excel file.
    try:
        df.to_excel(f"{filename}.xlsx", index=False)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
