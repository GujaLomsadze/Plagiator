import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'dbname': 'postgres'
        }
        self.target_db = os.getenv('DB_NAME')

    def _get_connection(self, autocommit=False):
        conn = psycopg2.connect(**self.conn_params)
        if autocommit:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn

    def reset_database(self):
        """Drop and recreate the target database"""
        try:
            conn = self._get_connection(autocommit=True)
            cursor = conn.cursor()

            cursor.execute(
                sql.SQL("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s
                AND pid <> pg_backend_pid();
                """), [self.target_db])

            # Drop and recreate the database
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(self.target_db)))
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.target_db)))

            print(f"Database {self.target_db} has been reset successfully.")
            return True

        except Exception as e:
            print(f"Error resetting database: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def execute_sql(self, sql_commands):
        """Execute SQL commands against the target database"""
        try:
            # Connect to the target database
            self.conn_params['dbname'] = self.target_db
            conn = self._get_connection()
            cursor = conn.cursor()

            for command in sql_commands:
                try:
                    cursor.execute(command)
                    conn.commit()
                    print(f"Executed successfully: {command[:50]}...")  # Truncate long SQL
                except Exception as e:
                    conn.rollback()
                    print(f"Error executing command: {command[:50]}...")
                    print(f"Error details: {e}")
                    return False

            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
