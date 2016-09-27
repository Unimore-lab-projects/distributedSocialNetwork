-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
object: "socialDB" | type: DATABASE
DROP DATABASE IF EXISTS "socialDB";
CREATE DATABASE "socialDB"
;
-- -- ddl-end --
-- 

-- object: public."myPost" | type: TABLE --
-- DROP TABLE IF EXISTS public."myPost" CASCADE;
CREATE TABLE "myPost"(
	"postID" timestamp NOT NULL,
	"userID" uuid,
	CONSTRAINT "PK" PRIMARY KEY ("postID")

);
-- ddl-end --
ALTER TABLE public."myPost" OWNER TO postgres;
-- ddl-end --

-- object: public."knownNodes" | type: TABLE --
-- DROP TABLE IF EXISTS public."knownNodes" CASCADE;
CREATE TABLE public."knownNodes"(
	"userID" uuid NOT NULL,
	"nodeIP" cidr,
	"portNumber" int4,
	username text,
	CONSTRAINT "PK_2" PRIMARY KEY ("userID")

);
-- ddl-end --
ALTER TABLE public."knownNodes" OWNER TO postgres;
-- ddl-end --

-- object: public.comment | type: TABLE --
-- DROP TABLE IF EXISTS public.comment CASCADE;
CREATE TABLE public.comment(
	"userID" uuid,
	"timestamp" timestamp,
	content text,
	"postID" integer,

);
-- ddl-end --
ALTER TABLE public.comment OWNER TO postgres;
-- ddl-end --

-- object: public.friend | type: TABLE --
-- DROP TABLE IF EXISTS public.friend CASCADE;
CREATE TABLE public.friend(
	"userID_knownNodes" uuid NOT NULL,
	CONSTRAINT friend_pk PRIMARY KEY ("userID_knownNodes")

);
-- ddl-end --
ALTER TABLE public.friend OWNER TO postgres;
-- ddl-end --

-- object: public."myUser" | type: TABLE --
-- DROP TABLE IF EXISTS public."myUser" CASCADE;
CREATE TABLE public."myUser"(
	"myID" uuid NOT NULL,
	"myUsername" text,
	"myAddress" cidr,
	"myPort" smallint,
	CONSTRAINT pk PRIMARY KEY ("myID")

);
-- ddl-end --
ALTER TABLE public."myUser" OWNER TO postgres;
-- ddl-end --

-- object: "knownNodes_fk" | type: CONSTRAINT --
-- ALTER TABLE public.friend DROP CONSTRAINT IF EXISTS "knownNodes_fk" CASCADE;
ALTER TABLE public.friend ADD CONSTRAINT "knownNodes_fk" FOREIGN KEY ("userID_knownNodes")
REFERENCES public."knownNodes" ("userID") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: friend_uq | type: CONSTRAINT --
-- ALTER TABLE public.friend DROP CONSTRAINT IF EXISTS friend_uq CASCADE;
ALTER TABLE public.friend ADD CONSTRAINT friend_uq UNIQUE ("userID_knownNodes");
-- ddl-end --

-- object: "fkUserID" | type: CONSTRAINT --
-- ALTER TABLE public."myPost" DROP CONSTRAINT IF EXISTS "fkUserID" CASCADE;
ALTER TABLE public."myPost" ADD CONSTRAINT "fkUserID" FOREIGN KEY ("userID")
REFERENCES public."myUser" ("myID") MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: "fkPostID" | type: CONSTRAINT --
-- ALTER TABLE public.comment DROP CONSTRAINT IF EXISTS "fkPostID" CASCADE;
ALTER TABLE public.comment ADD CONSTRAINT "fkPostID" FOREIGN KEY ("postID")
REFERENCES public."myPost" ("postID") MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: "fkUserID" | type: CONSTRAINT --
-- ALTER TABLE public.comment DROP CONSTRAINT IF EXISTS "fkUserID" CASCADE;
ALTER TABLE public.comment ADD CONSTRAINT "fkUserID" FOREIGN KEY ("userID")
REFERENCES public.friend ("userID_knownNodes") MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


