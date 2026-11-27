-- Optional plan inspection with a populated PostgreSQL database.
-- These are illustrative workload queries, not the archived benchmark commands.
EXPLAIN (ANALYZE, BUFFERS)
SELECT feeding_id, feed_date, feeding_amount_kg FROM public.feeding_records
WHERE a_id = 'A001' ORDER BY feed_date DESC LIMIT 10;

EXPLAIN (ANALYZE, BUFFERS)
SELECT record_id, datetime, weight FROM public.animal_state_record
WHERE a_id = 'A001' ORDER BY datetime DESC LIMIT 10;
