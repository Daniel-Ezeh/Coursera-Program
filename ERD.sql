-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE public.sales_transaction
(
    transaction_id integer NOT NULL,
    transaction_date date NOT NULL,
    transaction_time time without time zone NOT NULL,
    sales_outlet_id integer,
    staff_id integer,
    customer_id integer,
    PRIMARY KEY (transaction_id)
);

CREATE TABLE public.product
(
    product_id integer NOT NULL,
    product_name character varying(50),
    description character varying(200),
    price numeric(3, 2),
    PRIMARY KEY (product_id)
);

CREATE TABLE public.sales_detail
(
    sales_detail_id integer NOT NULL,
    product_id integer,
    quantity integer,
    price numeric,
    transaction_id integer,
    PRIMARY KEY (sales_detail_id)
);

CREATE TABLE public.product_type
(
    product_type_id integer NOT NULL,
    product_category character varying(30) NOT NULL,
    product_type character varying(50),
    product_id integer,
    PRIMARY KEY (product_type_id)
);

ALTER TABLE public.sales_detail
    ADD FOREIGN KEY (transaction_id)
    REFERENCES public.sales_transaction (transaction_id)
    NOT VALID;


ALTER TABLE public.sales_detail
    ADD FOREIGN KEY (product_id)
    REFERENCES public.product (product_id)
    NOT VALID;


ALTER TABLE public.product_type
    ADD FOREIGN KEY (product_id)
    REFERENCES public.product (product_id)
    NOT VALID;

END;