create table instruments (
id int auto_increment primary key,
UUID text not null,
instrument_id text not null,
name text not null,
type int not null,
notes mediumtext,
repair boolean,
active boolean,
created_at timestamp default now(),
updated_at timestamp,
deleted_at timestamp
);

create table loans (
instrument_id int,
foreign key (instrument_id) references instruments(id),
student_id int,
foreign key (student_id) references students(id),
created_at timestamp default now()
);

create table loans_history (
  instrument_id int,
  student_id int,
  lented_at timestamp,
  returned_at timestamp
);

create table users(
id int auto_increment primary key,
uuid text not null,
name text not null,
surname text,
username text not null,
permission_group int,
foreign key (permission_group) references groups(id),
active boolean,
created_at timestamp default now(),
updated_at timestamp,
deleted_at timestamp
);

create table groups (
id int auto_increment primary key,
uuid text not null,
name text not null,
permissions mediumtext,
active boolean,
created_at timestamp default now(),
updated_at timestamp,
deleted_at timestamp
);

drop table users;
drop table groups;