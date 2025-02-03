import argparse
import csv

from mk8d_stats_tracker.database import db

def export_data_to_csv(file_path):
    sessions = db.sessions.all()
    if not sessions:
        print("No data found in the database.")
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["date", "user_id", "start_vr", "end_vr", "races"])

        # Write the data
        for session in sessions:
            writer.writerow([
                session.get("date"),
                session.get("user_id"),
                session.get("start_vr"),
                session.get("end_vr"),
                session.get("races")
            ])

    print(f"Data exported to {file_path}")

def main():
    parser = argparse.ArgumentParser(description="MK8D Stats Tracker CLI")
    parser.add_argument('command', choices=['export'], help="Command to execute")
    parser.add_argument('--file', type=str, required=True, help="Output CSV file path")

    args = parser.parse_args()

    if args.command == 'export':
        export_data_to_csv(args.file)

if __name__ == "__main__":
    main()