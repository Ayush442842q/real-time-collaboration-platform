from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from typing import Dict

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teams = relationship('TeamMember', back_populates='user')
    messages = relationship('Message', back_populates='user')
    files = relationship('File', back_populates='user')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    members = relationship('TeamMember', back_populates='team')
    messages = relationship('Message', back_populates='team')
    files = relationship('File', back_populates='team')
    whiteboard = relationship('Whiteboard', back_populates='team')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class TeamMember(Base):
    __tablename__ = 'team_members'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = relationship('Team', back_populates='members')
    user = relationship('User', back_populates='teams')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = relationship('Team', back_populates='messages')
    user = relationship('User', back_populates='messages')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = relationship('Team', back_populates='files')
    user = relationship('User', back_populates='files')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Whiteboard(Base):
    __tablename__ = 'whiteboards'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = relationship('Team', back_populates='whiteboard')

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'team_id': self.team_id,
            'data': self.data,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Create engine
engine = create_engine('sqlite:///collaboration_platform.db')

# Create tables
Base.metadata.create_all(engine)