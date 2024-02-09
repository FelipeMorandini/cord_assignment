import json
import pandas as pd

def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def time_to_minutes(time_str):
    """Convert time from 'day.offset.hours:minutes' format to total minutes."""
    day, time = time_str.split('.')
    hours, minutes = map(int, time.split(':'))
    return int(day) * 24 * 60 + hours * 60 + minutes

def format_time(minutes):
    """Convert total minutes back into 'day.offset.hours:minutes' format."""
    days = minutes // (24 * 60)
    remaining_minutes = minutes % (24 * 60)
    hours = remaining_minutes // 60
    minutes = remaining_minutes % 60
    return f"{days}.{hours:02d}:{minutes:02d}"

def find_stop_name_by_id(stop_id, stops):
    """Return the stop name given a stop ID."""
    for stop in stops:
        if stop['stop_id'] == stop_id:
            return stop['stop_name']
    return "Unknown Stop"

def compare_times(time1, time2):
    """
    Compare two times in 'day.offset.hours:minutes' format.
    Returns True if time1 is before time2, else False.
    """
    return time_to_minutes(time1) < time_to_minutes(time2)

def print_report(report):
    """Prints the detailed report."""
    for duty in report:
        print(f"Duty ID: {duty['Duty ID']}, Start Time: {duty['Start Time']}, End Time: {duty['End Time']}, "
              f"First Stop: {duty['First Stop']}, Last Stop: {duty['Last Stop']}")
        for break_info in duty['Breaks']:
            print(f"\tBreak Start Time: {break_info['break_start_time']}, Duration: {break_info['break_duration']} minutes, "
                  f"Stop Name: {break_info['break_stop_name']}")

def calculate_breaks(vehicle_events, stops):
    """Calculate breaks between vehicle events."""
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

def export_to_excel(data, filename, step):
    """Export report data to an Excel file."""
    # Convert the data into a pandas DataFrame.
    if step == 1:
        columns = ['Duty ID', 'Start Time', 'End Time']
        df = pd.DataFrame(data, columns=columns)
    elif step == 2:
        # Flatten the data structure if necessary and create a DataFrame.
        df = pd.DataFrame(data)[['Duty ID', 'Start Time', 'End Time', 'First Stop', 'Last Stop']]
        df = pd.DataFrame(data)
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
    
    # Write the DataFrame to an Excel file.
    df.to_excel(f"{filename}.xlsx", index=False)
