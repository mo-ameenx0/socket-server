import sqlalchemy as db
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from constants import *

load_dotenv()
SECRET = os.environ.get('SECRET')

engine = db.create_engine("sqlite:///users.sqlite")
conn = engine.connect()
metadata = db.MetaData()

users_table = db.Table(
    'USERS', metadata,
    db.Column('ID', db.Integer(), primary_key=True, autoincrement=True),
    db.Column('NAME', db.VARCHAR(50), nullable=False),
    db.Column('PASSWORD', db.VARCHAR(150), nullable=False)
)

sessions_table = db.Table(
    'SESSIONS', metadata,
    db.Column('ID', db.Integer(), primary_key=True, autoincrement=True),
    db.Column('SESSION_ID', db.TEXT(), nullable=False),
    db.Column('USER_ID', db.Integer(), db.ForeignKey('USERS.ID'), nullable=False),
)

metadata.create_all(engine)

def signup_user(name, password):   
    if is_user_signed_up(name):
        return {RESPONSE: 'user already signed up'}
    
    cur = conn.execute(
        users_table.insert().values(
            NAME=name,
            PASSWORD=password
        )
    )

    conn.commit()

    return {RESPONSE: f'welcome {name} you are now signed up'}

def login_user(name, password):
    if not is_user_signed_up(name):
        return {RESPONSE: 'user is not signed up'}
    
    cur = conn.execute(
        users_table.select().where(
            users_table.columns.NAME == name,
            users_table.columns.PASSWORD == password
        )
    )

    user = cur.fetchone()

    if not user:
        return {RESPONSE: 'wrong password'}

    user_id = user[0]

    if is_user_loged_in(user_id):
        return {RESPONSE: 'user already loged in'}

    session_id = jwt.encode(
        {
            'name': name, 
            'user_id': user_id, 
            'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=5000)
        },
        SECRET
    )

    conn.execute(
        sessions_table.insert().values(
            SESSION_ID=session_id,
            USER_ID=user_id
        )
    )

    conn.commit()

    return {
        SESSION_ID: session_id,
        RESPONSE: f'welcome {name} you are now loged in'
    }

def logout_user(name, user_id):
    cur = conn.execute(
        sessions_table.select().where(sessions_table.columns.USER_ID == user_id)
    )

    if not cur.fetchone():
        return {RESPONSE: f'{name} already loged out'}


    cur = conn.execute(
       sessions_table.delete().where(sessions_table.columns.USER_ID == user_id)
    )

    conn.commit()

    return {
        RESPONSE: f'see you again {name}'
    }

def delete_user_session(session_id):
    cur = conn.execute(
       sessions_table.delete().where(sessions_table.columns.SESSION_ID == session_id)
    )

    conn.commit()

def is_user_signed_up(name):
    cur = conn.execute(
        users_table.select().where(users_table.columns.NAME == name)
    )

    if cur.fetchone():
        return True

    return False

def is_user_loged_in(user_id):
    cur = conn.execute(
        sessions_table.select().where(sessions_table.columns.USER_ID == user_id)
    )

    if cur.fetchone():
        return True
    
    return False

def is_user_loged_out(session_id):
    cur = conn.execute(
        sessions_table.select().where(sessions_table.columns.SESSION_ID == session_id)
    )

    if cur.fetchone():
        return False
    
    return True
