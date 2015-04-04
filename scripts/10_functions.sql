create or replace function add_message(
	type text
	, service text
	, "group" text
	, sender text
	, priority text
	, body text
	, format text
)
returns int as
$$

DECLARE

new_message_id int;

BEGIN

insert into messages(id, type, service, "group", sender, priority, body, format)
values (DEFAULT, type, service, "group", sender, priority, body, format)
returning id into new_message_id;

return new_message_id;

END

$$ language plpgsql;
