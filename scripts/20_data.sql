insert into message_sources (
	type
	, service
	, config
) 
values 
('irc', 'bnc.foo.net', '{"server":"bnc.foo.net", "channels":["general"]}');

select add_message(1, '#general', 'someguy', 'ping', 'hey, what you doin', 'plain');
select add_message(1, '#general', 'a.n.other', 'normal', 'this is a message', 'plain');

