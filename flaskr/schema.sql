drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  firstname text not null,
  lastname text not null,
  charity text not null,
  about text not null,
  email text not null
);