-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: "distributedSocialDB" | type: DATABASE --
-- -- DROP DATABASE IF EXISTS "distributedSocialDB";
-- CREATE DATABASE "distributedSocialDB"
-- 	OWNER = postgres
-- ;
-- -- ddl-end --
-- 

-- object: public.known_nodes | type: TABLE --
DROP TABLE IF EXISTS public.known_nodes CASCADE;
CREATE TABLE public.known_nodes (
  user_id     UUID NOT NULL,
  username    VARCHAR(16),
  address     CIDR,
  port        SMALLINT,
  last_update TIMESTAMP,
  CONSTRAINT "PK" PRIMARY KEY (user_id)

);
-- ddl-end --
ALTER TABLE public.known_nodes
  OWNER TO postgres;
-- ddl-end --

-- object: public.friends | type: TABLE --
DROP TABLE IF EXISTS public.friends CASCADE;
CREATE TABLE public.friends (
  user_id_known_nodes UUID,
  CONSTRAINT friends_pk PRIMARY KEY (user_id_known_nodes)

);
-- ddl-end --
ALTER TABLE public.friends
  OWNER TO postgres;
-- ddl-end --

-- object: known_nodes_fk | type: CONSTRAINT --
ALTER TABLE public.friends
  DROP CONSTRAINT IF EXISTS known_nodes_fk CASCADE;
ALTER TABLE public.friends
  ADD CONSTRAINT known_nodes_fk FOREIGN KEY (user_id_known_nodes)
REFERENCES public.known_nodes (user_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: public.comments | type: TABLE --
DROP TABLE IF EXISTS public.comments CASCADE;
CREATE TABLE public.comments (
  comment_id TIMESTAMP NOT NULL,
  content    VARCHAR(512),
  user_id    UUID,
  post_id    TIMESTAMP,
  CONSTRAINT comments_pk PRIMARY KEY (comment_id)
);
-- ddl-end --
ALTER TABLE public.comments
  OWNER TO postgres;
-- ddl-end --

-- object: public.posts | type: TABLE --
DROP TABLE IF EXISTS public.posts CASCADE;
CREATE TABLE public.posts (
  post_id TIMESTAMP NOT NULL,
  user_id UUID,
  CONSTRAINT post_pk PRIMARY KEY (post_id)
);
-- ddl-end --
ALTER TABLE public.posts
  OWNER TO postgres;
-- ddl-end --

-- object: public.post_img | type: TABLE --
DROP TABLE IF EXISTS public.post_img CASCADE;
CREATE TABLE public.post_img (
  path_to_file VARCHAR(512)
  --   post_id      TIMESTAMP NOT NULL,
  --   user_id      UUID
)
  INHERITS (public.posts);
-- ddl-end --
ALTER TABLE public.post_img
  OWNER TO postgres;
-- ddl-end --

-- object: public.post_text | type: TABLE --
DROP TABLE IF EXISTS public.post_text CASCADE;
CREATE TABLE public.post_text (
  content VARCHAR(512)
  --   post_id timestamp NOT NULL,
  --   user_id uuid
)
  INHERITS (public.posts);
-- ddl-end --
ALTER TABLE public.post_text
  OWNER TO postgres;
-- ddl-end --

-- object: public.my_user | type: TABLE --
DROP TABLE IF EXISTS public.my_user CASCADE;
CREATE TABLE public.my_user (
  user_id  UUID NOT NULL,
  username VARCHAR(16),
  CONSTRAINT my_user_pk PRIMARY KEY (user_id)

);
-- ddl-end --
ALTER TABLE public.my_user
  OWNER TO postgres;
-- ddl-end --

-- object: comments_post_id_fk | type: CONSTRAINT --
ALTER TABLE public.comments
  DROP CONSTRAINT IF EXISTS comments_post_id_fk CASCADE;
ALTER TABLE public.comments
  ADD CONSTRAINT comments_post_id_fk FOREIGN KEY (post_id)
REFERENCES public.posts (post_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: comments_user_id_fk | type: CONSTRAINT --
ALTER TABLE public.comments
  DROP CONSTRAINT IF EXISTS comments_user_id_fk CASCADE;
ALTER TABLE public.comments
  ADD CONSTRAINT comments_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.friends (user_id_known_nodes) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: post_user_id_fk | type: CONSTRAINT --
ALTER TABLE public.posts
  DROP CONSTRAINT IF EXISTS post_user_id_fk CASCADE;
ALTER TABLE public.posts
  ADD CONSTRAINT post_user_id_fk FOREIGN KEY (user_id)
REFERENCES public.my_user (user_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


