from pathlib import Path
from utils import export_to_excel, load_json_data
from steps import generate_start_end_times, generate_stop_names, generate_breaks_info

"""
Generates a series of Excel reports from JSON data in 3 steps:

1. Generate start and end times for duties and export 
2. Add stop names and export
3. Add break information and export full report

The main steps call helper functions to generate and process 
the data before exporting to Excel after each step.
"""
if __name__ == '__main__':
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / 'data'
    filepath = data_dir / 'mini_json_dataset.json'
    json_data = load_json_data(filepath)

    # Step 1: Generate start and end times and export
    print("Generating Step 1 XLSX file...")
    start_end_times = generate_start_end_times(json_data['duties'], json_data['vehicles'])
    export_to_excel(start_end_times, data_dir / 'step1', step=1)

    # Step 2: Add stop names and export
    print("Generating Step 2 XLSX file...")
    start_end_with_stop_names = generate_stop_names(start_end_times, json_data['stops'])
    export_to_excel(start_end_with_stop_names, data_dir / 'step2', step=2)

    # Step 3: Add break information and export
    print("Generating Step 3 XLSX file...")
    full_report = generate_breaks_info(start_end_with_stop_names, json_data['vehicles'], json_data['stops'])
    export_to_excel(full_report, data_dir / 'step3', step=3)