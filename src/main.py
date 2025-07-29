import os
import json
from database import DatabaseManager
from file_processor import SQLFileProcessor

AAL_FILE = "aal.json"

def load_aal():
    if os.path.exists(AAL_FILE):
        with open(AAL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_aal(aal):
    with open(AAL_FILE, "w") as f:
        json.dump(aal, f, indent=2)

def main(sql_scripts_path: str):
    db_manager = DatabaseManager()
    file_processor = SQLFileProcessor()

    print("Resetting database...")
    if not db_manager.reset_database():
        print("Failed to reset database. Exiting.")
        return

    sql_files = file_processor.get_sql_files(sql_scripts_path)
    if not sql_files:
        print("No SQL files found in the specified folder.")
        return

    print(f"Found {len(sql_files)} SQL files to process:")

    aal = load_aal()
    
    for sql_file in sql_files:
        if aal.get(sql_file) == "success":
            print(f"[AAL] Skipping already successful file: {sql_file}")
            continue
        print(f"\nProcessing file: {sql_file}")
        commands = file_processor.read_sql_commands(sql_file)

        if db_manager.execute_sql(commands):
            aal[sql_file] = "success"
            save_aal(aal)
        else:
            aal[sql_file] = "failed"
            save_aal(aal)
            print(f"Failed to execute commands from {sql_file}. Stopping.")
            break

    print("\nDatabase initialization complete.")


if __name__ == "__main__":
    main(sql_scripts_path="../sql_scripts")
