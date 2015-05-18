drop table if exists entries;
drop table if exists userPassword;
drop table if exists comments;

-- store entries
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  sdate text not null,
  -- stime text not null,
  start_time timestamp default current_timestamp not null,
  edate text not null,
  -- etime text not null
  end_time timestamp
);

-- store user information
create table userPassword (
  username text not null unique,
  password text not null,
  emailAddr text,
  flag_admin boolean not null default false,
  flag_approval boolean not null default false
);

-- store comments on entries
create table comments (
  comment_id integer primary key autoincrement,
  comment_input text(200),
  entry_id integer,
  username text not null,
  foreign key (entry_id) references entries(id)
);
