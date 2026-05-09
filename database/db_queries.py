import sqlite3
from sqlite3 import Error

class DatabaseQueries:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            print(f"Connected to SQLite Database {db_name}")
        except Error as e:
            print(e)

    def create_user(self, username, password, email):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_user(self, user_id, username, password, email):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Users SET username = ?, password = ?, email = ? WHERE id = ?", (username, password, email, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_team(self, name, description):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Teams (name, description) VALUES (?, ?)", (name, description))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_team(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Teams WHERE id = ?", (team_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_team(self, team_id, name, description):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Teams SET name = ?, description = ? WHERE id = ?", (name, description, team_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_team(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Teams WHERE id = ?", (team_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_teams(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Teams")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def add_team_member(self, team_id, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Team_Members (team_id, user_id) VALUES (?, ?)", (team_id, user_id))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_team_members(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Team_Members WHERE team_id = ?", (team_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_virtual_whiteboard(self, team_id, name, description):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Virtual_Whiteboards (team_id, name, description) VALUES (?, ?, ?)", (team_id, name, description))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_virtual_whiteboard(self, whiteboard_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Virtual_Whiteboards WHERE id = ?", (whiteboard_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_virtual_whiteboard(self, whiteboard_id, team_id, name, description):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Virtual_Whiteboards SET team_id = ?, name = ?, description = ? WHERE id = ?", (team_id, name, description, whiteboard_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_virtual_whiteboard(self, whiteboard_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Virtual_Whiteboards WHERE id = ?", (whiteboard_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_virtual_whiteboards(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Virtual_Whiteboards")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_document(self, team_id, name, content):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Documents (team_id, name, content) VALUES (?, ?, ?)", (team_id, name, content))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_document(self, document_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Documents WHERE id = ?", (document_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_document(self, document_id, team_id, name, content):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Documents SET team_id = ?, name = ?, content = ? WHERE id = ?", (team_id, name, content, document_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_document(self, document_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Documents WHERE id = ?", (document_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_documents(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Documents")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_task(self, team_id, name, description, status):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Tasks (team_id, name, description, status) VALUES (?, ?, ?, ?)", (team_id, name, description, status))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_task(self, task_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_task(self, task_id, team_id, name, description, status):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Tasks SET team_id = ?, name = ?, description = ?, status = ? WHERE id = ?", (team_id, name, description, status, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_task(self, task_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Tasks")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_message(self, team_id, user_id, content, timestamp):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Messages (team_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)", (team_id, user_id, content, timestamp))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_message(self, message_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Messages WHERE id = ?", (message_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_message(self, message_id, team_id, user_id, content, timestamp):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Messages SET team_id = ?, user_id = ?, content = ?, timestamp = ? WHERE id = ?", (team_id, user_id, content, timestamp, message_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_message(self, message_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Messages WHERE id = ?", (message_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_messages(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Messages")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_users(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username LIKE ? OR email LIKE ?", (f"%{query}%", f"%{query}%"))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_teams(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Teams WHERE name LIKE ?", (f"%{query}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_virtual_whiteboards(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Virtual_Whiteboards WHERE name LIKE ?", (f"%{query}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_documents(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Documents WHERE name LIKE ?", (f"%{query}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_tasks(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Tasks WHERE name LIKE ?", (f"%{query}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_messages(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Messages WHERE content LIKE ?", (f"%{query}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_users_in_team(self, team_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT U.* 
                FROM Users U 
                JOIN Team_Members TM ON U.id = TM.user_id 
                WHERE TM.team_id = ?
            """, (team_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_teams_with_virtual_whiteboards(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT T.* 
                FROM Teams T 
                JOIN Virtual_Whiteboards VW ON T.id = VW.team_id
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_teams_with_documents(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT T.* 
                FROM Teams T 
                JOIN Documents D ON T.id = D.team_id
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_teams_with_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT T.* 
                FROM Teams T 
                JOIN Tasks TS ON T.id = TS.team_id
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_teams_with_messages(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT T.* 
                FROM Teams T 
                JOIN Messages M ON T.id = M.team_id
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_users(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_teams(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Teams LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_virtual_whiteboards(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Virtual_Whiteboards LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_documents(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Documents LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_tasks(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Tasks LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def paginate_messages(self, limit, offset):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Messages LIMIT ? OFFSET ?", (limit, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    db = DatabaseQueries("collaboration.db")

    # Example usage
    user_id = db.create_user("john", "password", "john@example.com")
    print(f"Created user with ID: {user_id}")

    team_id = db.create_team("Team 1", "This is team 1")
    print(f"Created team with ID: {team_id}")

    db.add_team_member(team_id, user_id)

    virtual_whiteboard_id = db.create_virtual_whiteboard(team_id, "Whiteboard 1", "This is whiteboard 1")
    print(f"Created virtual whiteboard with ID: {virtual_whiteboard_id}")

    document_id = db.create_document(team_id, "Document 1", "This is document 1")
    print(f"Created document with ID: {document_id}")

    task_id = db.create_task(team_id, "Task 1", "This is task 1", "pending")
    print(f"Created task with ID: {task_id}")

    message_id = db.create_message(team_id, user_id, "Hello team!", "2022-01-01 12:00:00")
    print(f"Created message with ID: {message_id}")

    users = db.get_all_users()
    print("All users:")
    for user in users:
        print(user)

    teams = db.get_all_teams()
    print("All teams:")
    for team in teams:
        print(team)

    virtual_whiteboards = db.get_all_virtual_whiteboards()
    print("All virtual whiteboards:")
    for virtual_whiteboard in virtual_whiteboards:
        print(virtual_whiteboard)

    documents = db.get_all_documents()
    print("All documents:")
    for document in documents:
        print(document)

    tasks = db.get_all_tasks()
    print("All tasks:")
    for task in tasks:
        print(task)

    messages = db.get_all_messages()
    print("All messages:")
    for message in messages:
        print(message)

    db.conn.close()