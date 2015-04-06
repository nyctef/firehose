create or replace function add_message(
	source_id int
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

insert into messages(id, source_id, "group", sender, priority, body, format)
values (DEFAULT, source_id, "group", sender, priority, body, format)
returning id into new_message_id;

return new_message_id;

END

$$ language plpgsql;
