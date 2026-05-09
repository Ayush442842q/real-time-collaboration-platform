import sqlite3
from sqlite3 import Error

class DatabaseMigration:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self.create_migration_table()
        except Error as e:
            print(e)

    def create_migration_table(self):
        """Create migration tracking table"""
        query = """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                applied_at TEXT NOT NULL
            );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def apply_migration(self, name, query_up, query_down):
        """Apply a migration"""
        try:
            # Check if migration has already been applied
            self.cursor.execute("SELECT * FROM migrations WHERE name = ?", (name,))
            if self.cursor.fetchone():
                print(f"Migration {name} has already been applied.")
                return

            # Apply migration
            self.cursor.execute(query_up)
            self.conn.commit()
            self.cursor.execute("INSERT INTO migrations (name, applied_at) VALUES (?, datetime('now'))", (name,))
            self.conn.commit()
            print(f"Migration {name} applied successfully.")
        except Error as e:
            print(f"Error applying migration {name}: {e}")
            self.conn.rollback()

    def rollback_migration(self, name, query_down):
        """Rollback a migration"""
        try:
            # Check if migration has been applied
            self.cursor.execute("SELECT * FROM migrations WHERE name = ?", (name,))
            if not self.cursor.fetchone():
                print(f"Migration {name} has not been applied.")
                return

            # Rollback migration
            self.cursor.execute(query_down)
            self.conn.commit()
            self.cursor.execute("DELETE FROM migrations WHERE name = ?", (name,))
            self.conn.commit()
            print(f"Migration {name} rolled back successfully.")
        except Error as e:
            print(f"Error rolling back migration {name}: {e}")
            self.conn.rollback()

    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

def main():
    db_file = "database.db"
    migration = DatabaseMigration(db_file)

    # Create tables in correct dependency order
    migrations = [
        {
            "name": "create_users_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Users;"
        },
        {
            "name": "create_teams_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Teams;"
        },
        {
            "name": "create_team_members_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Team_Members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    team_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    UNIQUE (team_id, user_id)
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Team_Members;"
        },
        {
            "name": "create_virtual_whiteboards_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Virtual_Whiteboards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    team_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Virtual_Whiteboards;"
        },
        {
            "name": "create_documents_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    team_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    content TEXT,
                    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Documents;"
        },
        {
            "name": "create_tasks_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    team_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Tasks;"
        },
        {
            "name": "create_messages_table",
            "query_up": """
                CREATE TABLE IF NOT EXISTS Messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    team_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            """,
            "query_down": "DROP TABLE IF EXISTS Messages;"
        },
        {
            "name": "create_indexes",
            "query_up": """
                CREATE INDEX IF NOT EXISTS idx_Team_Members_team_id ON Team_Members (team_id);
                CREATE INDEX IF NOT EXISTS idx_Virtual_Whiteboards_team_id ON Virtual_Whiteboards (team_id);
                CREATE INDEX IF NOT EXISTS idx_Documents_team_id ON Documents (team_id);
                CREATE INDEX IF NOT EXISTS idx_Tasks_team_id ON Tasks (team_id);
                CREATE INDEX IF NOT EXISTS idx_Messages_team_id ON Messages (team_id);
            """,
            "query_down": """
                DROP INDEX IF EXISTS idx_Team_Members_team_id;
                DROP INDEX IF EXISTS idx_Virtual_Whiteboards_team_id;
                DROP INDEX IF EXISTS idx_Documents_team_id;
                DROP INDEX IF EXISTS idx_Tasks_team_id;
                DROP INDEX IF EXISTS idx_Messages_team_id;
            """
        }
    ]

    for migration in migrations:
        migration.apply_migration(migration["name"], migration["query_up"], migration["query_down"])

    migration.close_connection()

if __name__ == "__main__":
    main()