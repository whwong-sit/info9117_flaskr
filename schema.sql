drop table if exists entries;
create table entries (
  id INTEGER PRIMARY KEY autoincrement,
  title text NOT NULL,
  text text NOT NULL,
  username text NOT NULL,
  start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_time TIMESTAMP
  sdate text NOT NULL,
  stime text NOT NULL,
  edate text NOT NULL,
  etime text NOT NULL
  );
drop table if exists comments;
create table comments (
  comment_id INTEGER PRIMARY KEY autoincrement,
  comment_input TEXT(200),
  entry_id INTEGER,
  username text NOT NULL,
  FOREIGN KEY (entry_id) REFERENCES entries(id)
);

create table userPassword (
  username text not null,
  password text not null
);

