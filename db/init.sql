SET CHARSET UTF8;
DROP DATABASE IF EXISTS tasker;

CREATE DATABASE tasker;

use tasker;

CREATE TABLE jobs (
  rid VARCHAR(50),
  client_name VARCHAR(20),
  task_name VARCHAR(50),
  task_params VARCHAR(100),
  status VARCHAR(50),
  result VARCHAR(100),
  error VARCHAR(50),
  client_ip VARCHAR(50),
  created_at INTEGER,
  updated_at INTEGER
);


CREATE TABLE job_events (
  rid VARCHAR(50),
  event_name VARCHAR(50),
  created_at INTEGER,
  updated_at INTEGER,
  primary key (rid, event_name)
);



CREATE TABLE process_config (
  name VARCHAR(50),
  status VARCHAR(50),
  created_at INTEGER,
  updated_at INTEGER
);

INSERT INTO process_config
  (name, status)
VALUES
  ('sum2', 'active'),
  ('surprise', 'active'),
  ('mult3', 'active');
