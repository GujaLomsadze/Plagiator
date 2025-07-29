import os


class SQLFileProcessor:
    @staticmethod
    def get_sql_files(folder_path):
        """Get all .sql files from folder sorted by name"""
        files = [f for f in os.listdir(folder_path) if f.endswith('.sql')]
        files.sort()
        return [os.path.join(folder_path, f) for f in files]

    @staticmethod
    def read_sql_commands(file_path):
        """Read SQL file and split into individual commands"""
        with open(file_path, 'r') as file:
            content = file.read()

        # Split by semicolon and remove empty/whitespace-only commands
        commands = [cmd.strip() for cmd in content.split(';') if cmd.strip()]
        return commands
