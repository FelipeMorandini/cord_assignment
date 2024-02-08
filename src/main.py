from pathlib import Path
from utils import export_to_excel, load_json_data, print_report
from steps import generate_start_end_times, generate_stop_names, generate_breaks_info

if __name__ == '__main__':
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / 'data'
    filepath = data_dir / 'mini_json_dataset.json'  # Update this path to your JSON file location
    json_data = load_json_data(filepath)

    # Step 1: Generate start and end times
    start_end_times = generate_start_end_times(json_data['duties'], json_data['vehicles'], json_data['stops'])
    export_to_excel(start_end_times, data_dir / 'step1')

    # Step 2: Add stop names
    start_end_with_stop_names = generate_stop_names(start_end_times, json_data['stops'])
    export_to_excel(start_end_with_stop_names, data_dir / 'step2')

    # Step 3: Add break information
    full_report = generate_breaks_info(start_end_with_stop_names, json_data['vehicles'], json_data['stops'])
    export_to_excel(full_report, data_dir / 'step3')

    print_report(full_report)