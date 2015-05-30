drop table if exists entries;
drop table if exists userPassword;
drop table if exists comments;
drop table if exists userRoles;

-- store entries
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  start_time timestamp default (datetime(current_timestamp,'localtime')),
  end_time timestamp
);

-- store user information
create table userPassword (
  username text not null,
  password text not null,
  gravataremail text not null
);

-- store comments on entries
create table comments (
  comment_id integer primary key autoincrement,
  comment_input text(200),
  entry_id integer,
  username text not null,
  comment_time timestamp default (datetime(current_timestamp,'localtime')),
  foreign key (entry_id) references entries(id)
);

create table userRoles(
role_id integer primary key autoincrement,
user_role text,
entry_id integer,
foreign key (entry_id) references entries(id)
)
