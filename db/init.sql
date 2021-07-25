dIF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'tasker')
BEGIN
CREATE DATABASE tasker
END

use tasker;

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='jobs')
BEGIN
CREATE TABLE jobs (
  rid VARCHAR(50),
  client_name VARCHAR(20),
  task_name VARCHAR(50),
  task_params VARCHAR(100),
  status VARCHAR(50),
  error VARCHAR(50),
  client_ip VARCHAR(50),
  create_at INTEGER,
  updated_at INTEGER
)
END

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='job_events')
BEGIN
CREATE TABLE job_events (
  rid VARCHAR(50),
  event_name VARCHAR(50),
  create_at INTEGER,
  updated_at INTEGER,
  primary key (rid, event_name)
)
END

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='process_config')
BEGIN
CREATE TABLE process_config (
  name VARCHAR(50),
  status VARCHAR(50),
  create_at INTEGER,
  updated_at INTEGER
)
END

INSERT INTO process_config
  (name, status)
VALUES
  ('sum2', 'active'),
  ('surprise', 'active'),
  ('multiply3', 'active');

INSERT INTO mysql.user (Host, User, Password) VALUES ('%', 'root', password('root'));
GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION;