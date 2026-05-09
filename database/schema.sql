-- Drop existing tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Teams;
DROP TABLE IF EXISTS Team_Members;
DROP TABLE IF EXISTS Virtual_Whiteboards;
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS Messages;

-- Create Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create Teams table
CREATE TABLE Teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Create Team_Members table
CREATE TABLE Team_Members (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (team_id, user_id)
);

-- Create Virtual_Whiteboards table
CREATE TABLE Virtual_Whiteboards (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    team_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Documents table
CREATE TABLE Documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    team_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    content TEXT,
    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Tasks table
CREATE TABLE Tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    team_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Messages table
CREATE TABLE Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES Teams (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create indexes
CREATE INDEX idx_Team_Members_team_id ON Team_Members (team_id);
CREATE INDEX idx_Virtual_Whiteboards_team_id ON Virtual_Whiteboards (team_id);
CREATE INDEX idx_Documents_team_id ON Documents (team_id);
CREATE INDEX idx_Tasks_team_id ON Tasks (team_id);
CREATE INDEX idx_Messages_team_id ON Messages (team_id);

-- Insert sample data
INSERT INTO Users (username, password, email) VALUES ('john', 'password', 'john@example.com');
INSERT INTO Users (username, password, email) VALUES ('jane', 'password', 'jane@example.com');

INSERT INTO Teams (name, description) VALUES ('Team 1', 'This is team 1');
INSERT INTO Teams (name, description) VALUES ('Team 2', 'This is team 2');

INSERT INTO Team_Members (team_id, user_id) VALUES (1, 1);
INSERT INTO Team_Members (team_id, user_id) VALUES (1, 2);
INSERT INTO Team_Members (team_id, user_id) VALUES (2, 1);

INSERT INTO Virtual_Whiteboards (team_id, name, description) VALUES (1, 'Whiteboard 1', 'This is whiteboard 1');
INSERT INTO Virtual_Whiteboards (team_id, name, description) VALUES (2, 'Whiteboard 2', 'This is whiteboard 2');

INSERT INTO Documents (team_id, name, content) VALUES (1, 'Document 1', 'This is document 1');
INSERT INTO Documents (team_id, name, content) VALUES (2, 'Document 2', 'This is document 2');

INSERT INTO Tasks (team_id, name, description, status) VALUES (1, 'Task 1', 'This is task 1', 'pending');
INSERT INTO Tasks (team_id, name, description, status) VALUES (2, 'Task 2', 'This is task 2', 'completed');

INSERT INTO Messages (team_id, user_id, content, timestamp) VALUES (1, 1, 'Hello team!', '2022-01-01 12:00:00');
INSERT INTO Messages (team_id, user_id, content, timestamp) VALUES (1, 2, 'Hi!', '2022-01-01 12:05:00');