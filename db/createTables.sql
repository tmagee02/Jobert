-- create table Company (
--     id integer primary key,
--     company_name text not null,
--     base_url text not null unique,
--     search_path text not null,
--     search_query text,
--     date_added datetime default current_timestamp
-- );

-- create table Job (
--     id integer primary key, 
--     job_url text not null unique,
--     title text not null,
--     job_desc text not null,
--     min_experience integer,
--     max_experience integer,
--     date_added datetime default current_timestamp,
--     company_id integer not null,
--     foreign key (company_id) references Company(id) on delete cascade
-- );

-- alter table Job rename column date_added to date_scraped;
-- alter table Job add column date_posted datetime;

-- create table Location (
--     id integer primary key,
--     location_name text not null,
--     is_remote boolean default false
-- );

-- create table JobLocation (
--     job_id integer not null,
--     location_id integer not null,
--     primary key (job_id, location_id),
--     foreign key (job_id) references Job(id) on delete cascade,
--     foreign key (location_id) references Location(id) on delete cascade
-- );



