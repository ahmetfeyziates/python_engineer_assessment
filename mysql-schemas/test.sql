drop table if exists examples;

create table `examples` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  primary key (`id`)
);

drop table if exists person;

create table `person` (
  `id` int not null auto_increment,
  `name` varchar(80) not null,
  `age` int not null,
  `city` varchar(80) not null,
  `interest1` varchar(256) default null,
  `interest2` varchar(256) default null,
  `interest3` varchar(256) default null,
  `interest4` varchar(256) default null,
  `phone_number` varchar(32) not null,
  primary key (`id`)
);