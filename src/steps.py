from src.utils import calculate_breaks, time_to_minutes, find_stop_name_by_id, compare_times


"""Generates start and end times for each duty by looking at all vehicle events.

For each duty, finds the earliest start time and latest end time from events with a matching duty ID.
Returns a list of dicts with duty ID, start time, and end time for each duty.
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

"""Generates stop names for each duty by looking up the stop IDs.

For each duty, finds the stop name corresponding to the first and last stop IDs.
Returns the updated start/end times list with stop names added.
"""
def generate_stop_names(start_end_times, stops):
    for duty_data in start_end_times:
        first_stop_id = duty_data.get('First Stop ID')
        last_stop_id = duty_data.get('Last Stop ID')
        
        first_stop_name = find_stop_name_by_id(first_stop_id, stops) if first_stop_id else "Unknown Stop"
        last_stop_name = find_stop_name_by_id(last_stop_id, stops) if last_stop_id else "Unknown Stop"
        
        duty_data['First Stop'] = first_stop_name
        duty_data['Last Stop'] = last_stop_name
    return start_end_times

"""Generates break details for each duty.

For each duty, finds the vehicle events matching the duty ID, sorts them, calculates the breaks between the events, and adds the break details to the duty data.

Returns the updated start/end times list with break details added for each duty.
"""
def generate_breaks_info(start_end_with_stop_names, vehicles, stops):
    for duty_data in start_end_with_stop_names:
        duty_id = duty_data['Duty ID']
        vehicle_events = [
            event for vehicle in vehicles for event in vehicle['vehicle_events']
            if event.get('duty_id') == duty_id and 'start_time' in event and 'end_time' in event
        ]
        vehicle_events_sorted = sorted(vehicle_events, key=lambda x: time_to_minutes(x['start_time']))
        breaks = calculate_breaks(vehicle_events_sorted, stops)
        duty_data['Breaks'] = breaks
    return start_end_with_stop_names
