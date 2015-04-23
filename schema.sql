drop table if exists entries;
drop table if exists userPassword;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  sdate text not null,
  stime text not null,
  edate text not null,
  etime text not null
);

create table entries (
username text not null,
password text not null
);