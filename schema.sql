drop table if exists entries;
create table entries (
  id INTEGER PRIMARY KEY autoincrement,
  title text NOT NULL,
  text text NOT NULL,
  username text NOT NULL,
  start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  );

create table comments (
  comment_id INTEGER PRIMARY KEY autoincrement,
  comment_input TEXT(200),
  entry_id INTEGER,
  FOREIGN KEY (entry_id) REFERENCES entries(id)
);




