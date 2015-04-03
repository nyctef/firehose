insert into messages (
	"type"
	, service
	, "group"
	, sender
	, priority
	, body
	, format )
values
('irc', 'bnc.foo.net', '#general', 'someguy', 'ping', 'hey, what you doin', 'plain')
