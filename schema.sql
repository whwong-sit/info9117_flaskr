drop table if exists entries;
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

