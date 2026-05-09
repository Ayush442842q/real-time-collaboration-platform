# app.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import jwt
import datetime
from typing import Optional

# Initialize the FastAPI app
app = FastAPI()

# Initialize the CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Initialize the database connection
DATABASE_NAME = os.environ.get("DATABASE_NAME", "collaboration_platform.db")

# Initialize the secret key for JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key")

# Define the User model
class User(BaseModel):
    id: int
    username: str
    email: str

# Define the Team model
class Team(BaseModel):
    id: int
    name: str
    description: str

# Define the Message model
class Message(BaseModel):
    id: int
    team_id: int
    content: str

# Define the File model
class File(BaseModel):
    id: int
    team_id: int
    file_name: str
    file_type: str

# Define the Whiteboard model
class Whiteboard(BaseModel):
    id: int
    team_id: int
    data: str

# Create the database tables if they do not exist
def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY,
            team_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            team_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            team_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS whiteboards (
            id INTEGER PRIMARY KEY,
            team_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )"""
    )
    conn.commit()
    conn.close()

create_tables()

# Function to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return User(id=user[0], username=user[1], email=user[2])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# Function to authenticate a user
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    user = c.fetchone()
    conn.close()
    if user is None or user[3] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = user[0]
    payload = {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# API endpoint to create a new user
@app.post("/api/v1/users")
async def create_user(username: str, password: str, email: str):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()
    return {"id": c.lastrowid, "username": username, "email": email}

# API endpoint to get a list of all users
@app.get("/api/v1/users")
async def get_users(current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return [{"id": user[0], "username": user[1], "email": user[2]} for user in users]

# API endpoint to create a new team
@app.post("/api/v1/teams")
async def create_team(name: str, description: str, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE name = ?", (name,))
    team = c.fetchone()
    if team is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    c.execute("INSERT INTO teams (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()
    return {"id": c.lastrowid, "name": name, "description": description}

# API endpoint to get a list of all teams
@app.get("/api/v1/teams")
async def get_teams(current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    conn.close()
    return [{"id": team[0], "name": team[1], "description": team[2]} for team in teams]

# API endpoint to add a new member to a team
@app.post("/api/v1/teams/{team_id}/members")
async def add_member(team_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM team_members WHERE team_id = ? AND user_id = ?", (team_id, user_id))
    member = c.fetchone()
    if member is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    c.execute("INSERT INTO team_members (team_id, user_id) VALUES (?, ?)", (team_id, user_id))
    conn.commit()
    conn.close()
    return {"id": c.lastrowid, "team_id": team_id, "user_id": user_id}

# API endpoint to get a list of all members of a team
@app.get("/api/v1/teams/{team_id}/members")
async def get_members(team_id: int, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM team_members WHERE team_id = ?", (team_id,))
    members = c.fetchall()
    conn.close()
    return [{"id": member[0], "team_id": member[1], "user_id": member[2]} for member in members]

# API endpoint to send a new message to a team
@app.post("/api/v1/teams/{team_id}/messages")
async def send_message(team_id: int, content: str, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("INSERT INTO messages (team_id, content) VALUES (?, ?)", (team_id, content))
    conn.commit()
    conn.close()
    return {"id": c.lastrowid, "team_id": team_id, "content": content}

# API endpoint to get a list of all messages sent to a team
@app.get("/api/v1/teams/{team_id}/messages")
async def get_messages(team_id: int, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM messages WHERE team_id = ?", (team_id,))
    messages = c.fetchall()
    conn.close()
    return [{"id": message[0], "team_id": message[1], "content": message[2]} for message in messages]

# API endpoint to upload a new file to a team
@app.post("/api/v1/teams/{team_id}/files")
async def upload_file(team_id: int, file_name: str, file_type: str, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("INSERT INTO files (team_id, file_name, file_type) VALUES (?, ?, ?)", (team_id, file_name, file_type))
    conn.commit()
    conn.close()
    return {"id": c.lastrowid, "team_id": team_id, "file_name": file_name, "file_type": file_type}

# API endpoint to get a list of all files uploaded to a team
@app.get("/api/v1/teams/{team_id}/files")
async def get_files(team_id: int, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM files WHERE team_id = ?", (team_id,))
    files = c.fetchall()
    conn.close()
    return [{"id": file[0], "team_id": file[1], "file_name": file[2], "file_type": file[3]} for file in files]

# API endpoint to get the whiteboard data for a team
@app.get("/api/v1/teams/{team_id}/whiteboard")
async def get_whiteboard(team_id: int, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM whiteboards WHERE team_id = ?", (team_id,))
    whiteboard = c.fetchone()
    conn.close()
    if whiteboard is None:
        return {"id": 0, "team_id": team_id, "data": ""}
    return {"id": whiteboard[0], "team_id": whiteboard[1], "data": whiteboard[2]}

# API endpoint to update the whiteboard data for a team
@app.post("/api/v1/teams/{team_id}/whiteboard")
async def update_whiteboard(team_id: int, data: str, current_user: User = Depends(get_current_user)):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = c.fetchone()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    c.execute("SELECT * FROM whiteboards WHERE team_id = ?", (team_id,))
    whiteboard = c.fetchone()
    if whiteboard is None:
        c.execute("INSERT INTO whiteboards (team_id, data) VALUES (?, ?)", (team_id, data))
    else:
        c.execute("UPDATE whiteboards SET data = ? WHERE team_id = ?", (data, team_id))
    conn.commit()
    conn.close()
    return {"id": whiteboard[0] if whiteboard else c.lastrowid, "team_id": team_id, "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)