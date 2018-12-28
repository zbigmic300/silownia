-- create tables
create table users (
  id numeric constraint pk_users primary key,
  created_date timestamp not null,
  updated_date timestamp,
  removed_date timestamp,
  status varchar(1) not null,
  login varchar(100) not null constraint un_users_login unique,
  password varchar(100) not null,
  admin boolean not null default false,
  first_name varchar(100),
  last_name varchar(100),
  room varchar(3),
  last_login_date timestamp,
  booked_interval interval not null default '0',
  last_reservation_date timestamp
);

create table reservations (
  id integer constraint pk_reservations primary key,
  created_date timestamp not null,
  user_id integer constraint fk_users references users(id),
  start_date timestamp not null,
  end_date timestamp not null
);

create table revoked_tokens (
  id integer constraint pk_revoked_tokens primary key,
  created_date timestamp not null,
  jti varchar(255) not null,
  expire_date timestamp not null
);

-- create sequences
create sequence seq_users_id;
create sequence seq_reservations_id;
create sequence seq_revoked_tokens_id;

-- init admin user
insert into users (
  id, created_date, status, login, password, admin, first_name, last_name, room)
values (
  nextval('seq_users_id'), current_timestamp at time zone 'utc', 'A', 'admin', encode(sha256('Admin1'), 'hex'),
  true, 'admin', 'admin', '0');
commit;
