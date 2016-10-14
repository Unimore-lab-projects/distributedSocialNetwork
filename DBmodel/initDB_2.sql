DROP DATABASE IF EXISTS mydatabase;
 CREATE DATABASE mydatabase
 	ENCODING = 'UTF8'
 	LC_COLLATE = 'it_IT.UTF8'
 	LC_CTYPE = 'it_IT.UTF8'
 	TABLESPACE = pg_default
-- 	OWNER = archeffect
 ;

CREATE TABLE comments
(
    content VARCHAR(512),
    user_id UUID NOT NULL,
    id INTEGER PRIMARY KEY NOT NULL,
    comment_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    username VARCHAR(16),
    CONSTRAINT comments_friends_user_id_fk FOREIGN KEY (user_id) REFERENCES ,
    CONSTRAINT comments_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES
);
CREATE UNIQUE INDEX comments_user_id_uindex ON comments (user_id);
CREATE UNIQUE INDEX comments_id_uindex ON comments (id);
CREATE UNIQUE INDEX comments_comment_id_uindex ON comments (comment_id);
CREATE TABLE friends
(
    user_id UUID NOT NULL,
    username VARCHAR(16),
    id INTEGER PRIMARY KEY NOT NULL,
    CONSTRAINT friends_known_nodes_user_id_fk FOREIGN KEY (user_id) REFERENCES
);
CREATE UNIQUE INDEX friends_user_id_uindex ON friends (user_id);
CREATE UNIQUE INDEX friends_id_uindex ON friends (id);
CREATE TABLE known_nodes
(
    user_id UUID NOT NULL,
    address CIDR NOT NULL,
    port SMALLINT NOT NULL,
    last_update TIMESTAMP NOT NULL,
    id INTEGER PRIMARY KEY NOT NULL
);
CREATE UNIQUE INDEX known_nodes_user_id_uindex ON known_nodes (user_id);
CREATE TABLE my_user
(
    user_id UUID NOT NULL,
    username VARCHAR(16),
    id INTEGER PRIMARY KEY NOT NULL
);
CREATE UNIQUE INDEX my_user_user_id_uindex ON my_user (user_id);
CREATE TABLE posts
(
    user_id UUID NOT NULL,
    path_to_imagefile VARCHAR(512),
    text_content VARCHAR(512),
    id INTEGER PRIMARY KEY NOT NULL,
    post_id BIGINT NOT NULL,
    CONSTRAINT posts_my_user_user_id_fk FOREIGN KEY (user_id) REFERENCES
);
CREATE UNIQUE INDEX posts_id_uindex ON posts (path_to_imagefile);
CREATE UNIQUE INDEX posts_post_id_uindex ON posts (text_content);