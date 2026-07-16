DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS readings;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS current;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    moisture REAL,
    irrigation INTEGER DEFAULT 0,
    crop TEXT DEFAULT 'None'
);

CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    irrigation_status INTEGER DEFAULT 0,
    selected_crop TEXT DEFAULT 'None'
);

INSERT INTO settings (id, irrigation_status, selected_crop) VALUES (1, 0, 'None');
