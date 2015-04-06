drop table if exists messages;
drop table if exists message_sources;

create table message_sources (
	id serial primary key not null
	, "type" text not null
	, service text not null
	, config jsonb not null
);

create table messages (
	id serial primary key not null
	, source_id int not null references message_sources(id)
	, "group" text null
	, sender text null
	, priority text null
	, body text not null
	, format text not null
);


