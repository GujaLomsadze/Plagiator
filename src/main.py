from database import DatabaseManager
from file_processor import SQLFileProcessor


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

    for sql_file in sql_files:
        print(f"\nProcessing file: {sql_file}")
        commands = file_processor.read_sql_commands(sql_file)

        if not db_manager.execute_sql(commands):
            print(f"Failed to execute commands from {sql_file}. Stopping.")
            break

    print("\nDatabase initialization complete.")


if __name__ == "__main__":
    main(sql_scripts_path="../sql_scripts")
