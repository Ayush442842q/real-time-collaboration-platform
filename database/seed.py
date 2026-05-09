import sqlite3
from datetime import datetime, timedelta

def create_seed_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert users
    users = [
        ('john_doe', 'password123', 'john@example.com'),
        ('jane_doe', 'password123', 'jane@example.com'),
        ('bob_smith', 'password123', 'bob@example.com'),
        ('alice_johnson', 'password123', 'alice@example.com'),
        ('mike_brown', 'password123', 'mike@example.com'),
    ]

    c.executemany('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', users)

    # Insert teams
    teams = [
        ('Team 1', 'This is team 1'),
        ('Team 2', 'This is team 2'),
        ('Team 3', 'This is team 3'),
        ('Team 4', 'This is team 4'),
        ('Team 5', 'This is team 5'),
    ]

    c.executemany('INSERT INTO Teams (name, description) VALUES (?, ?)', teams)

    # Insert team members
    team_members = [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 4),
        (3, 2),
        (3, 3),
        (3, 5),
        (4, 1),
        (4, 2),
        (5, 3),
        (5, 4),
        (5, 5),
    ]

    c.executemany('INSERT INTO Team_Members (team_id, user_id) VALUES (?, ?)', team_members)

    # Insert virtual whiteboards
    virtual_whiteboards = [
        (1, 'Whiteboard 1', 'This is whiteboard 1'),
        (2, 'Whiteboard 2', 'This is whiteboard 2'),
        (3, 'Whiteboard 3', 'This is whiteboard 3'),
        (4, 'Whiteboard 4', 'This is whiteboard 4'),
        (5, 'Whiteboard 5', 'This is whiteboard 5'),
    ]

    c.executemany('INSERT INTO Virtual_Whiteboards (team_id, name, description) VALUES (?, ?, ?)', virtual_whiteboards)

    # Insert documents
    documents = [
        (1, 'Document 1', 'This is document 1'),
        (2, 'Document 2', 'This is document 2'),
        (3, 'Document 3', 'This is document 3'),
        (4, 'Document 4', 'This is document 4'),
        (5, 'Document 5', 'This is document 5'),
    ]

    c.executemany('INSERT INTO Documents (team_id, name, content) VALUES (?, ?, ?)', documents)

    # Insert tasks
    tasks = [
        (1, 'Task 1', 'This is task 1', 'pending'),
        (2, 'Task 2', 'This is task 2', 'completed'),
        (3, 'Task 3', 'This is task 3', 'pending'),
        (4, 'Task 4', 'This is task 4', 'completed'),
        (5, 'Task 5', 'This is task 5', 'pending'),
    ]

    c.executemany('INSERT INTO Tasks (team_id, name, description, status) VALUES (?, ?, ?, ?)', tasks)

    # Insert messages
    messages = [
        (1, 1, 'Hello team!', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, 2, 'Hi!', (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')),
        (2, 1, 'Hello team 2!', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, 2, 'Hi team 3!', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, 1, 'Hello team 4!', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, 3, 'Hi team 5!', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, 3, 'Hello team 1 again!', (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')),
        (2, 4, 'Hi team 2 again!', (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')),
        (3, 5, 'Hello team 3 again!', (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')),
        (4, 2, 'Hi team 4 again!', (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')),
        (5, 1, 'Hello team 5 again!', (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')),
    ]

    c.executemany('INSERT INTO Messages (team_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)', messages)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == '__main__':
    create_seed_data()