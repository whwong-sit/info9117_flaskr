drop table if exists entries;
drop table if exists userPassword;
create table entries (
<<<<<<< HEAD
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  sdate text not null,
  stime text not null,
  edate text not null,
  etime text not null
);

create table userPassword (
  username text not null,
  password text not null
=======
  id INTEGER PRIMARY KEY autoincrement,
  title text NOT NULL,
  text text NOT NULL,
  username text NOT NULL,
  start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_time TIMESTAMP
  );
drop table if exists comments;
create table comments (
  comment_id INTEGER PRIMARY KEY autoincrement,
  comment_input TEXT(200),
  entry_id INTEGER,
  username text NOT NULL,
  FOREIGN KEY (entry_id) REFERENCES entries(id)
>>>>>>> d19ef11f1b10b276e9737d1bfd7c657b01791a38
);