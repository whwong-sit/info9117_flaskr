drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  );

create table comments (
  comment_id integer primary key autoincrement,
  comment_input text(200),
  Related_entry_id INTEGER
);

create table entry_has_comments
(entry_id integer primary key,
comment_id integer,
foreign key (entry_id) references entries(id),
foreign key (comment_id) references comments(comment_id)
);




