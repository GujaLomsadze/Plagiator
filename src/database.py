import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


class DatabaseManager:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'dbname': 'template1' # Always connecting to this `template1` database
        }
        self.target_db = os.getenv('DB_NAME')

    def _get_connection(self, autocommit=False, target_db=None):
        """Get connection, optionally to a specific database"""
        params = self.conn_params.copy()
        if target_db:
            params['dbname'] = target_db

        conn = psycopg2.connect(**params)
        if autocommit:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn

    def reset_database(self):
        """Drop and recreate the target database"""
        try:
            # Connect to default postgres database to perform reset
            conn = self._get_connection(autocommit=True)
            cursor = conn.cursor()

            # Terminate existing connections to the target DB
            terminate_sql = sql.SQL("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s
            AND pid <> pg_backend_pid();
            """)

            console.print(f"[yellow]Terminating connections to {self.target_db}...[/yellow]")
            cursor.execute(terminate_sql, [self.target_db])

            # Drop and recreate the database
            console.print(f"[yellow]Dropping database {self.target_db}...[/yellow]")
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(self.target_db)))

            console.print(f"[green]Creating database {self.target_db}...[/green]")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.target_db)))

            console.print(f"[bold green]Database {self.target_db} has been reset successfully.[/bold green]")
            return True
        except Exception as e:
            console.print(f"[red]Error resetting database: {e}[/red]")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def execute_sql(self, sql_commands):
        """Execute SQL commands against the target database"""
        try:
            # Connect to the target database for execution
            conn = self._get_connection(target_db=self.target_db)
            cursor = conn.cursor()

            for command in sql_commands:
                try:
                    console.print(f"[dim]Executing: {command[:100]}...[/dim]")
                    cursor.execute(command)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    console.print(f"[red]Error executing command: {e}[/red]")
                    console.print(f"[red]Failed command: {command[:200]}[/red]")
                    return False

            return True
        except Exception as e:
            console.print(f"[red]Database error: {e}[/red]")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def test_connection(self):
        """Test database connection"""
        try:
            conn = self._get_connection()
            conn.close()
            return True
        except Exception as e:
            console.print(f"[red]Connection failed: {e}[/red]")
            return False
