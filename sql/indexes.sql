-- Composite B-tree indexes used in the team project.
CREATE INDEX idx_animal_state_record_aid_datetime ON public.animal_state_record USING btree (a_id, datetime DESC);
CREATE INDEX idx_feeding_records_aid_feeddate ON public.feeding_records USING btree (a_id, feed_date DESC);
