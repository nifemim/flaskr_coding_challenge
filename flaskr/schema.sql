drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  firstname text,
  lastname text,
  charity text,
  about text,
  email text,
  hitcount integer,
  dob date,
  post_title text
);
