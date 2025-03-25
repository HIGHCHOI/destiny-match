from flask import current_app, g
import sqlite3
from passlib.hash import pbkdf2_sha256

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def register_user(email, username, password):
    db = get_db()
    hashed = pbkdf2_sha256.hash(password)
    db.execute(
        "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
        (email, username, hashed)
    )
    db.commit()

def get_user_by_email(email):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

def update_profile(user_id, name, age, gender, mbti, hobbies, music_style,
                   height, weight, personality, appearance, body_shape,
                   ideal_age_diff, ideal_mbti, ideal_personality, ideal_appearance,
                   ideal_height_range, ideal_weight_range, ideal_body_shape):
    db = get_db()
    db.execute("""
        UPDATE users SET name=?, age=?, gender=?, mbti=?, hobbies=?, music_style=?,
            height=?, weight=?, personality=?, appearance=?, body_shape=?,
            ideal_age_diff=?, ideal_mbti=?, ideal_personality=?, ideal_appearance=?,
            ideal_height_range=?, ideal_weight_range=?, ideal_body_shape=?
        WHERE id=?
    """, (name, age, gender, mbti, hobbies, music_style,
          height, weight, personality, appearance, body_shape,
          ideal_age_diff, ideal_mbti, ideal_personality, ideal_appearance,
          ideal_height_range, ideal_weight_range, ideal_body_shape, user_id))
    db.commit()


def get_all_users_except(current_user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id != ?", (current_user_id,)).fetchall()

def get_all_users_except(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id != ?", (user_id,)).fetchall()

