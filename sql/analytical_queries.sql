-- Representative queries for the original application workflows.
-- Run after loading a compatible dataset; A001 and E003 are example identifiers.
-- Latest feeding history
SELECT feeding_id, feed_date, f_id, feeding_amount_kg
FROM public.feeding_records WHERE a_id = 'A001'
ORDER BY feed_date DESC LIMIT 10;

-- Latest health observations
SELECT record_id, datetime, weight, state_id
FROM public.animal_state_record WHERE a_id = 'A001'
ORDER BY datetime DESC LIMIT 10;

-- Daily weight trend in the most recent 30-day window of the loaded dataset
SELECT DATE(datetime) AS day, AVG(weight) AS average_weight_kg
FROM public.animal_state_record
WHERE a_id = 'A001' AND datetime >= (SELECT MAX(datetime) FROM public.animal_state_record) - INTERVAL '30 days'
GROUP BY DATE(datetime) ORDER BY day;

-- Current stock from the signed inventory ledger
SELECT f.f_id, f.feed_name, COALESCE(SUM(i.quantity_delta_kg), 0) AS current_stock_kg
FROM public.feeds f LEFT JOIN public.feeding_inventory i ON i.f_id = f.f_id
GROUP BY f.f_id, f.feed_name ORDER BY current_stock_kg;

-- Employee assignments and task descriptions
SELECT es.shift_id, es.shift_start, es.shift_end, a.a_name, t.t_name
FROM public.employee_shift es
JOIN public.task t ON t.t_id = es.t_id
LEFT JOIN public.animal a ON a.a_id = es.a_id
WHERE es.e_id = 'E003' ORDER BY es.shift_start DESC;

-- Species-specific diet eligibility
SELECT a.a_id, a.species, f.f_id, f.feed_name
FROM public.animal a JOIN public.animal_diet d ON d.species = a.species
JOIN public.feeds f ON f.f_id = d.f_id WHERE a.a_id = 'A001';
