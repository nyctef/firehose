drop table if exists messages;

create table messages (
	id serial primary key
	, "type" text not null
	, service text not null
	, "group" text null
	, sender text null
	, priority text null
	, body text not null
	, format text not null
);


