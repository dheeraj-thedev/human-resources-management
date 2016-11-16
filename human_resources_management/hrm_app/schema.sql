DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS departments;
CREATE TABLE users (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  department_id INTEGER,
  position_id   INTEGER,
  email         TEXT NOT NULL,
  phone         TEXT NOT NULL,
  date_of_birth DATE NOT NULL
);
CREATE TABLE positions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  description TEXT NOT NULL
);
CREATE TABLE departments (
  id                     INTEGER PRIMARY KEY AUTOINCREMENT,
  name                   TEXT NOT NULL,
  parental_department_id INTEGER,
  leader_id              INTEGER,
  description            TEXT NOT NULL
);