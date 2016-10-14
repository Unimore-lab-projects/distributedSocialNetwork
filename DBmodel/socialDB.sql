-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---

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

-- object: public.friends_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.friends_id_seq CASCADE;
CREATE SEQUENCE public.friends_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.friends_id_seq OWNER TO archeffect;
-- ddl-end --

-- object: public.comments_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.comments_id_seq CASCADE;
CREATE SEQUENCE public.comments_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.comments_id_seq OWNER TO archeffect;
-- ddl-end --

-- object: public.posts_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.posts_id_seq CASCADE;
CREATE SEQUENCE public.posts_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.posts_id_seq OWNER TO archeffect;
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
	address cidr NOT NULL,
	port smallint NOT NULL,
	last_update timestamp NOT NULL,
	id integer NOT NULL DEFAULT nextval('public.known_nodes_id_seq'::regclass),
	CONSTRAINT known_nodes_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.known_nodes OWNER TO postgres;
-- ddl-end --

-- object: friends_id_uindex | type: INDEX --
-- DROP INDEX IF EXISTS public.friends_id_uindex CASCADE;
CREATE UNIQUE INDEX friends_id_uindex ON public.friends
	USING btree
	(
	  id
	)	WITH (FILLFACTOR = 90);
-- ddl-end --

-- object: comments_id_uindex | type: INDEX --
-- DROP INDEX IF EXISTS public.comments_id_uindex CASCADE;
CREATE UNIQUE INDEX comments_id_uindex ON public.comments
	USING btree
	(
	  id
	)	WITH (FILLFACTOR = 90);
-- ddl-end --

-- object: posts_id_uindex | type: INDEX --
-- DROP INDEX IF EXISTS public.posts_id_uindex CASCADE;
CREATE UNIQUE INDEX posts_id_uindex ON public.posts
	USING btree
	(
	  id
	)	WITH (FILLFACTOR = 90);
-- ddl-end --

-- object: public.friends | type: TABLE --
-- DROP TABLE IF EXISTS public.friends CASCADE;
CREATE TABLE public.friends(
	user_id uuid NOT NULL,
	username character varying(16),
	id integer NOT NULL DEFAULT nextval('public.friends_id_seq'::regclass),
	CONSTRAINT friends_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.friends OWNER TO postgres;
-- ddl-end --

-- object: public.posts | type: TABLE --
-- DROP TABLE IF EXISTS public.posts CASCADE;
CREATE TABLE public.posts(
	user_id uuid NOT NULL,
	path_to_imagefile character varying(512),
	text_content character varying(512),
	id integer NOT NULL DEFAULT nextval('public.posts_id_seq'::regclass),
	post_id bigint NOT NULL,
	CONSTRAINT posts_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.posts OWNER TO postgres;
-- ddl-end --

-- object: public.comments | type: TABLE --
-- DROP TABLE IF EXISTS public.comments CASCADE;
CREATE TABLE public.comments(
	content character varying(512),
	user_id uuid NOT NULL,
	id integer NOT NULL DEFAULT nextval('public.comments_id_seq'::regclass),
	comment_id bigint NOT NULL,
	post_id bigint NOT NULL,
	CONSTRAINT comments_id_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.comments OWNER TO postgres;
-- ddl-end --

-- object: comments_comment_id_uindex | type: INDEX --
-- DROP INDEX IF EXISTS public.comments_comment_id_uindex CASCADE;
CREATE UNIQUE INDEX comments_comment_id_uindex ON public.comments
	USING btree
	(
	  comment_id
	)	WITH (FILLFACTOR = 90);
-- ddl-end --

-- object: friends_known_nodes_user_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.friends DROP CONSTRAINT IF EXISTS friends_known_nodes_user_id_fk CASCADE;
ALTER TABLE public.friends ADD CONSTRAINT friends_known_nodes_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.known_nodes (user_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: comments_friends_user_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS comments_friends_user_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT comments_friends_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.friends (user_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: comments_posts_post_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS comments_posts_post_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT comments_posts_post_id_fk FOREIGN KEY (post_id)
REFERENCES public.posts (post_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: posts_my_user_user_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.posts DROP CONSTRAINT IF EXISTS posts_my_user_user_id_fk CASCADE;
ALTER TABLE public.posts ADD CONSTRAINT posts_my_user_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.my_user (user_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


