-- Course database schema (PostgreSQL 17). Run in a new, empty database.
-- Data and owner-specific dump commands are excluded.
BEGIN;

CREATE TABLE public.animal (
    a_id character varying(20) NOT NULL,
    species character varying(80) NOT NULL,
    sex character varying(10) NOT NULL,
    life_status character varying(20) NOT NULL,
    a_name character varying(50),
    CONSTRAINT animal_life_status_check CHECK (((life_status)::text = ANY (ARRAY[('Alive'::character varying)::text, ('Deceased'::character varying)::text, ('Transferred'::character varying)::text]))),
    CONSTRAINT animal_sex_check CHECK (((sex)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text, ('Unknown'::character varying)::text])))
);

CREATE TABLE public.animal_diet (
    species character varying NOT NULL,
    f_id character varying NOT NULL
);

CREATE TABLE public.animal_state_record (
    record_id character varying(20) NOT NULL,
    a_id character varying(20) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    weight numeric(7,2),
    state_id bigint NOT NULL,
    recorded_by character varying(20)
);

CREATE TABLE public.employee (
    e_id character varying(20) NOT NULL,
    e_name character varying(80) NOT NULL,
    sex character varying(10) NOT NULL,
    phone character varying(30),
    start_time timestamp without time zone,
    status character varying(20) NOT NULL,
    role character varying(20) DEFAULT 'User'::character varying,
    password_hash character varying(64),
    CONSTRAINT employee_sex_check CHECK (((sex)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text, ('Unknown'::character varying)::text]))),
    CONSTRAINT employee_status_check CHECK (((status)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text, ('leave'::character varying)::text])))
);

CREATE TABLE public.employee_shift (
    shift_id character varying(20) NOT NULL,
    e_id character varying(20) NOT NULL,
    t_id character varying(20) NOT NULL,
    shift_start timestamp without time zone NOT NULL,
    shift_end timestamp without time zone NOT NULL,
    a_id character varying(20)
);

CREATE TABLE public.employee_skills (
    skill_id integer NOT NULL,
    e_id character varying(20) NOT NULL,
    skill_name character varying(50) NOT NULL,
    issue_date date DEFAULT CURRENT_DATE
);

CREATE TABLE public.feeding_inventory (
    stock_entry_id character varying(20) NOT NULL,
    f_id character varying(20) NOT NULL,
    location_id character varying(20),
    datetime timestamp without time zone NOT NULL,
    quantity_delta_kg numeric(10,3) NOT NULL,
    reason character varying(30) NOT NULL,
    feeding_id character varying(20),
    CONSTRAINT feeding_inventory_reason_check CHECK (((reason)::text = ANY (ARRAY[('purchase'::character varying)::text, ('feeding'::character varying)::text, ('wastage'::character varying)::text, ('adjustment'::character varying)::text])))
);

CREATE TABLE public.feeding_records (
    feeding_id character varying(20) NOT NULL,
    a_id character varying(20) NOT NULL,
    f_id character varying(20) NOT NULL,
    fed_by character varying(20) NOT NULL,
    feed_date timestamp without time zone NOT NULL,
    feeding_amount_kg numeric(7,2) NOT NULL
);

CREATE TABLE public.feeds (
    f_id character varying(20) NOT NULL,
    feed_name character varying(80) NOT NULL,
    category character varying(40),
    CONSTRAINT feeds_category_check CHECK (((category)::text = ANY (ARRAY[('meat'::character varying)::text, ('plant'::character varying)::text, ('processed'::character varying)::text, ('other'::character varying)::text])))
);

CREATE TABLE public.species (
    s_name character varying(80) NOT NULL,
    required_skill character varying(50) DEFAULT 'General'::character varying
);

CREATE TABLE public.status_type (
    s_id bigint NOT NULL,
    s_name character varying(80) NOT NULL,
    description text
);

CREATE TABLE public.task (
    t_id character varying(20) NOT NULL,
    t_name character varying(80) NOT NULL
);

CREATE SEQUENCE public.animal_state_record_state_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.employee_skills_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.status_type_s_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.animal_state_record_state_id_seq OWNED BY public.animal_state_record.state_id;

ALTER SEQUENCE public.employee_skills_skill_id_seq OWNED BY public.employee_skills.skill_id;

ALTER SEQUENCE public.status_type_s_id_seq OWNED BY public.status_type.s_id;

ALTER TABLE ONLY public.animal_state_record ALTER COLUMN state_id SET DEFAULT nextval('public.animal_state_record_state_id_seq'::regclass);

ALTER TABLE ONLY public.employee_skills ALTER COLUMN skill_id SET DEFAULT nextval('public.employee_skills_skill_id_seq'::regclass);

ALTER TABLE ONLY public.status_type ALTER COLUMN s_id SET DEFAULT nextval('public.status_type_s_id_seq'::regclass);

ALTER TABLE ONLY public.animal_diet
    ADD CONSTRAINT animal_diet_pkey PRIMARY KEY (species, f_id);

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_pkey PRIMARY KEY (a_id);

ALTER TABLE ONLY public.animal_state_record
    ADD CONSTRAINT animal_state_record_pkey PRIMARY KEY (record_id);

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (e_id);

ALTER TABLE ONLY public.employee_shift
    ADD CONSTRAINT employee_shift_pkey PRIMARY KEY (shift_id);

ALTER TABLE ONLY public.employee_skills
    ADD CONSTRAINT employee_skills_pkey PRIMARY KEY (skill_id);

ALTER TABLE ONLY public.feeding_inventory
    ADD CONSTRAINT feeding_inventory_pkey PRIMARY KEY (stock_entry_id);

ALTER TABLE ONLY public.feeding_records
    ADD CONSTRAINT feeding_records_pkey PRIMARY KEY (feeding_id);

ALTER TABLE ONLY public.feeds
    ADD CONSTRAINT feeds_pkey PRIMARY KEY (f_id);

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (s_name);

ALTER TABLE ONLY public.status_type
    ADD CONSTRAINT status_type_pkey PRIMARY KEY (s_id);

ALTER TABLE ONLY public.status_type
    ADD CONSTRAINT status_type_s_name_key UNIQUE (s_name);

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (t_id);

ALTER TABLE ONLY public.employee_skills
    ADD CONSTRAINT unique_employee_skill UNIQUE (e_id, skill_name);

ALTER TABLE ONLY public.animal_diet
    ADD CONSTRAINT animal_diet_f_id_fkey FOREIGN KEY (f_id) REFERENCES public.feeds(f_id);

ALTER TABLE ONLY public.employee_skills
    ADD CONSTRAINT employee_skills_e_id_fkey FOREIGN KEY (e_id) REFERENCES public.employee(e_id) ON DELETE CASCADE;

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT fk_animal_species FOREIGN KEY (species) REFERENCES public.species(s_name) ON UPDATE CASCADE;

ALTER TABLE ONLY public.animal_diet
    ADD CONSTRAINT fk_diet_species FOREIGN KEY (species) REFERENCES public.species(s_name) ON UPDATE CASCADE;

ALTER TABLE ONLY public.feeding_records
    ADD CONSTRAINT fk_feeding_animal FOREIGN KEY (a_id) REFERENCES public.animal(a_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.feeding_records
    ADD CONSTRAINT fk_feeding_employee FOREIGN KEY (fed_by) REFERENCES public.employee(e_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.feeding_records
    ADD CONSTRAINT fk_feeding_feed FOREIGN KEY (f_id) REFERENCES public.feeds(f_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.feeding_inventory
    ADD CONSTRAINT fk_inventory_feed FOREIGN KEY (f_id) REFERENCES public.feeds(f_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.feeding_inventory
    ADD CONSTRAINT fk_inventory_feeding FOREIGN KEY (feeding_id) REFERENCES public.feeding_records(feeding_id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE ONLY public.employee_shift
    ADD CONSTRAINT fk_shift_animal FOREIGN KEY (a_id) REFERENCES public.animal(a_id);

ALTER TABLE ONLY public.employee_shift
    ADD CONSTRAINT fk_shift_employee FOREIGN KEY (e_id) REFERENCES public.employee(e_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.employee_shift
    ADD CONSTRAINT fk_shift_task FOREIGN KEY (t_id) REFERENCES public.task(t_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.animal_state_record
    ADD CONSTRAINT fk_state_record_animal FOREIGN KEY (a_id) REFERENCES public.animal(a_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.animal_state_record
    ADD CONSTRAINT fk_state_record_employee FOREIGN KEY (recorded_by) REFERENCES public.employee(e_id) ON UPDATE CASCADE ON DELETE SET NULL;

COMMIT;
