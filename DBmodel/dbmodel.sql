--
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: archeffect
--

CREATE SEQUENCE comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE comments (
    content character varying(512),
    user_id uuid NOT NULL,
    id integer DEFAULT nextval('comments_id_seq'::regclass) NOT NULL,
    comment_id bigint NOT NULL,
    post_id bigint NOT NULL,
    username character varying(16)
);



--
-- Name: friends_id_seq; Type: SEQUENCE; Schema: public; Owner: archeffect
--

CREATE SEQUENCE friends_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: friends; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE friends (
    user_id uuid NOT NULL,
    username character varying(16),
    id integer DEFAULT nextval('friends_id_seq'::regclass) NOT NULL
);



--
-- Name: known_nodes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE known_nodes (
    user_id uuid NOT NULL,
    address cidr NOT NULL,
    port smallint NOT NULL,
    last_update timestamp without time zone NOT NULL,
    id integer NOT NULL
);



--
-- Name: known_nodes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE known_nodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: known_nodes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE known_nodes_id_seq OWNED BY known_nodes.id;


--
-- Name: my_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE my_user (
    user_id uuid NOT NULL,
    username character varying(16),
    id integer NOT NULL
);



--
-- Name: my_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE my_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: my_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE my_user_id_seq OWNED BY my_user.id;


--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: archeffect
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE posts (
    user_id uuid NOT NULL,
    path_to_imagefile character varying(512),
    text_content character varying(512),
    id integer DEFAULT nextval('posts_id_seq'::regclass) NOT NULL,
    post_id bigint NOT NULL
);



--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY known_nodes ALTER COLUMN id SET DEFAULT nextval('known_nodes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY my_user ALTER COLUMN id SET DEFAULT nextval('my_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archeffect
--

SELECT pg_catalog.setval('comments_id_seq', 3, true);


--
-- Data for Name: friends; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- Name: friends_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archeffect
--

SELECT pg_catalog.setval('friends_id_seq', 2, true);


--
-- Data for Name: known_nodes; Type: TABLE DATA; Schema: public; Owner: postgres
--

--
-- Name: known_nodes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('known_nodes_id_seq', 14, true);


--
-- Data for Name: my_user; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- Name: my_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('my_user_id_seq', 8, true);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archeffect
--

SELECT pg_catalog.setval('posts_id_seq', 8, true);


--
-- Name: comments_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_id_pk PRIMARY KEY (id);


--
-- Name: friends_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY friends
    ADD CONSTRAINT friends_id_pk PRIMARY KEY (id);


--
-- Name: known_nodes_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY known_nodes
    ADD CONSTRAINT known_nodes_id_pk PRIMARY KEY (id);


--
-- Name: my_user_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY my_user
    ADD CONSTRAINT my_user_id_pk PRIMARY KEY (id);


--
-- Name: posts_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_id_pk PRIMARY KEY (id);


--
-- Name: comments_comment_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX comments_comment_id_uindex ON comments USING btree (comment_id);


--
-- Name: comments_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX comments_id_uindex ON comments USING btree (id);


--
-- Name: friends_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX friends_id_uindex ON friends USING btree (id);


--
-- Name: friends_user_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX friends_user_id_uindex ON friends USING btree (user_id);


--
-- Name: known_nodes_user_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX known_nodes_user_id_uindex ON known_nodes USING btree (user_id);


--
-- Name: my_user_user_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX my_user_user_id_uindex ON my_user USING btree (user_id);


--
-- Name: posts_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX posts_id_uindex ON posts USING btree (id);


--
-- Name: posts_post_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX posts_post_id_uindex ON posts USING btree (post_id);


--
-- Name: comments_friends_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_friends_user_id_fk FOREIGN KEY (user_id) REFERENCES friends(user_id);


--
-- Name: comments_posts_post_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES posts(post_id);


--
-- Name: friends_known_nodes_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY friends
    ADD CONSTRAINT friends_known_nodes_user_id_fk FOREIGN KEY (user_id) REFERENCES known_nodes(user_id);


--
-- Name: posts_my_user_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_my_user_user_id_fk FOREIGN KEY (user_id) REFERENCES my_user(user_id);


--
-- PostgreSQL database dump complete
--

