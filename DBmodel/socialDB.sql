-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---

-- object: archeffect | type: ROLE --
-- DROP ROLE IF EXISTS archeffect;
CREATE ROLE archeffect WITH 
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: mydatabase | type: DATABASE --
-- -- DROP DATABASE IF EXISTS mydatabase;
-- CREATE DATABASE mydatabase
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'it_IT.UTF8'
-- 	LC_CTYPE = 'it_IT.UTF8'
-- 	TABLESPACE = pg_default
-- 	OWNER = archeffect
-- ;
-- -- ddl-end --
-- 

-- object: public.known_nodes_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.known_nodes_id_seq CASCADE;
CREATE SEQUENCE public.known_nodes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.known_nodes_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.friends | type: TABLE --
-- DROP TABLE IF EXISTS public.friends CASCADE;
CREATE TABLE public.friends(
	user_id_known_nodes uuid NOT NULL,
	username character varying(16),
	CONSTRAINT friends_pk PRIMARY KEY (user_id_known_nodes)

);
-- ddl-end --
ALTER TABLE public.friends OWNER TO postgres;
-- ddl-end --

-- object: public.comments | type: TABLE --
-- DROP TABLE IF EXISTS public.comments CASCADE;
CREATE TABLE public.comments(
	comment_id timestamp NOT NULL,
	content character varying(512),
	user_id uuid,
	post_id timestamp,
	CONSTRAINT comments_pk PRIMARY KEY (comment_id)

);
-- ddl-end --
ALTER TABLE public.comments OWNER TO postgres;
-- ddl-end --

-- object: public.posts | type: TABLE --
-- DROP TABLE IF EXISTS public.posts CASCADE;
CREATE TABLE public.posts(
	post_id timestamp NOT NULL,
	user_id uuid,
	path_to_imagefile character varying(512),
	text_content character varying(512),
	CONSTRAINT post_pk PRIMARY KEY (post_id)

);
-- ddl-end --
ALTER TABLE public.posts OWNER TO postgres;
-- ddl-end --

-- object: public.my_user_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.my_user_id_seq CASCADE;
CREATE SEQUENCE public.my_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.my_user_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.my_user | type: TABLE --
-- DROP TABLE IF EXISTS public.my_user CASCADE;
CREATE TABLE public.my_user(
	user_id uuid NOT NULL,
	username character varying(16),
	id integer NOT NULL DEFAULT nextval('public.my_user_id_seq'::regclass),
	CONSTRAINT my_user_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.my_user OWNER TO postgres;
-- ddl-end --

-- object: public.known_nodes | type: TABLE --
-- DROP TABLE IF EXISTS public.known_nodes CASCADE;
CREATE TABLE public.known_nodes(
	user_id uuid NOT NULL,
	address cidr,
	port smallint,
	last_update timestamp,
	id integer NOT NULL DEFAULT nextval('public.known_nodes_id_seq'::regclass),
	CONSTRAINT known_nodes_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.known_nodes OWNER TO postgres;
-- ddl-end --

-- object: comments_post_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS comments_post_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT comments_post_id_fk FOREIGN KEY (post_id)
REFERENCES public.posts (post_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: comments_user_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS comments_user_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT comments_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.friends (user_id_known_nodes) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


