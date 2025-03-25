DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,

    name TEXT,
    age INTEGER,
    gender TEXT,
    mbti TEXT,
    hobbies TEXT,
    music_style TEXT,

    height INTEGER,
    weight INTEGER,
    personality TEXT,
    appearance TEXT,
    body_shape TEXT,

    ideal_age_diff INTEGER,
    ideal_mbti TEXT,
    ideal_personality TEXT,
    ideal_appearance TEXT,
    ideal_height_range TEXT,
    ideal_weight_range TEXT,
    ideal_body_shape TEXT
);

