from utils import calculate_breaks, time_to_minutes, format_time, find_stop_name_by_id, compare_times

"""
Generate start and end times for each duty based on the given duties and vehicles.

Parameters:
- duties (list): A list of dictionaries representing each duty.
- vehicles (list): A list of dictionaries representing each vehicle.

Returns:
- start_end_times (list): A list of dictionaries representing the start and end times for each duty.
"""
def generate_start_end_times(duties, vehicles):
    start_end_times = []
    for duty in duties:
        duty_id = duty['duty_id']
        earliest_start, latest_end = "23.59:59", "0.00:00"

        for vehicle in vehicles:
            for event in vehicle['vehicle_events']:
                if event.get('duty_id') == duty_id:
                    if 'start_time' in event:
                        if compare_times(event['start_time'], earliest_start) or earliest_start == "23.59:59":
                            earliest_start = event['start_time']
                    if 'end_time' in event:
                        if compare_times(latest_end, event['end_time']) or latest_end == "0.00:00":
                            latest_end = event['end_time']

        start_end_times.append({
            'Duty ID': duty_id,
            'Start Time': earliest_start if earliest_start != "23.59:59" else "No Start Time Found",
            'End Time': latest_end if latest_end != "0.00:00" else "No End Time Found",
        })
    return start_end_times

def generate_stop_names(start_end_times, stops):
    for duty_data in start_end_times:
        first_stop_id = duty_data.get('First Stop ID')
        last_stop_id = duty_data.get('Last Stop ID')
        
        first_stop_name = find_stop_name_by_id(first_stop_id, stops) if first_stop_id else "Unknown Stop"
        last_stop_name = find_stop_name_by_id(last_stop_id, stops) if last_stop_id else "Unknown Stop"
        
        duty_data['First Stop'] = first_stop_name
        duty_data['Last Stop'] = last_stop_name
    return start_end_times

def generate_breaks_info(start_end_with_stop_names, vehicles, stops):
    """Calculates breaks info for each duty and adds it to the report."""
    for duty_data in start_end_with_stop_names:
        duty_id = duty_data['Duty ID']
        # Filter vehicle events for the current duty
        vehicle_events = [
            event for vehicle in vehicles for event in vehicle['vehicle_events']
            if event.get('duty_id') == duty_id and 'start_time' in event and 'end_time' in event
        ]
        # Sort events by start time
        vehicle_events_sorted = sorted(vehicle_events, key=lambda x: time_to_minutes(x['start_time']))
        # Calculate breaks
        breaks = calculate_breaks(vehicle_events_sorted, stops)
        # Add breaks info to duty data
        duty_data['Breaks'] = breaks
    return start_end_with_stop_names
