CREATE TYPE task_status_enum as ENUM ('NEW', 'IN_PROGRESS', 'DONE', 'CANCELLED');

CREATE TABLE public.tasks (
    id uuid NOT NULL,
    name varchar NOT NULL,
    status task_status_enum NOT NULL DEFAULT 'NEW',
    description varchar NULL,
    author varchar NULL,
    date_created timestamp NOT NULL,
    date_updated timestamp NOT NULL,
    CONSTRAINT task_pk PRIMARY KEY (id)
    );