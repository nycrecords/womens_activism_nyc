--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

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
-- Name: comment_edit_types; Type: TYPE; Schema: public; Owner: sgong
--

CREATE TYPE comment_edit_types AS ENUM (
    'Edit',
    'Delete'
);


ALTER TYPE comment_edit_types OWNER TO sgong;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE alembic_version OWNER TO sgong;

--
-- Name: comment_edits; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE comment_edits (
    id integer NOT NULL,
    comment_id integer,
    user_id integer,
    edit_time timestamp without time zone NOT NULL,
    type comment_edit_types NOT NULL,
    content text NOT NULL,
    reason text NOT NULL
);


ALTER TABLE comment_edits OWNER TO sgong;

--
-- Name: comment_edits_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE comment_edits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comment_edits_id_seq OWNER TO sgong;

--
-- Name: comment_edits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE comment_edits_id_seq OWNED BY comment_edits.id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE comments (
    id integer NOT NULL,
    post_id integer NOT NULL,
    content character varying(750) NOT NULL,
    creation_time timestamp without time zone NOT NULL,
    is_edited boolean NOT NULL,
    is_visible boolean NOT NULL
);


ALTER TABLE comments OWNER TO sgong;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_id_seq OWNER TO sgong;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE comments_id_seq OWNED BY comments.id;


--
-- Name: feedback; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE feedback (
    id integer NOT NULL,
    title character varying(30) NOT NULL,
    email character varying(30),
    reason character varying(500) NOT NULL
);


ALTER TABLE feedback OWNER TO sgong;

--
-- Name: feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feedback_id_seq OWNER TO sgong;

--
-- Name: feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE feedback_id_seq OWNED BY feedback.id;


--
-- Name: flags; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE flags (
    id integer NOT NULL,
    post_id integer,
    type character varying(30),
    reason character varying(500) NOT NULL
);


ALTER TABLE flags OWNER TO sgong;

--
-- Name: flags_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE flags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE flags_id_seq OWNER TO sgong;

--
-- Name: flags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE flags_id_seq OWNED BY flags.id;


--
-- Name: post_edits; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE post_edits (
    id integer NOT NULL,
    post_id integer,
    user_id integer,
    edit_time timestamp without time zone NOT NULL,
    type character varying(6) NOT NULL,
    title character varying(140),
    content text NOT NULL,
    reason text NOT NULL,
    version integer
);


ALTER TABLE post_edits OWNER TO sgong;

--
-- Name: post_edits_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE post_edits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE post_edits_id_seq OWNER TO sgong;

--
-- Name: post_edits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE post_edits_id_seq OWNED BY post_edits.id;


--
-- Name: post_tags; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE post_tags (
    post_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE post_tags OWNER TO sgong;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE posts (
    id integer NOT NULL,
    activist_name character varying(30) NOT NULL,
    activist_start_date timestamp without time zone NOT NULL,
    activist_end_date timestamp without time zone NOT NULL,
    content text NOT NULL,
    author_name character varying(140) NOT NULL,
    author_email character varying(140) NOT NULL,
    author_website character varying(140) NOT NULL,
    creation_time timestamp without time zone NOT NULL,
    is_edited boolean NOT NULL,
    is_visible boolean NOT NULL,
    version integer
);


ALTER TABLE posts OWNER TO sgong;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE posts_id_seq OWNER TO sgong;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE roles (
    id integer NOT NULL,
    name character varying(64),
    "default" boolean,
    permissions integer
);


ALTER TABLE roles OWNER TO sgong;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE roles_id_seq OWNER TO sgong;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE roles_id_seq OWNED BY roles.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE tags (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE tags OWNER TO sgong;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tags_id_seq OWNER TO sgong;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE tags_id_seq OWNED BY tags.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: sgong
--

CREATE TABLE users (
    id integer NOT NULL,
    password_hash character varying(128),
    first_name character varying(30),
    last_name character varying(30),
    email character varying(50),
    phone character varying(11),
    role_id integer,
    confirmed boolean,
    site character varying(50),
    is_subscribed boolean
);


ALTER TABLE users OWNER TO sgong;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: sgong
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO sgong;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sgong
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comment_edits ALTER COLUMN id SET DEFAULT nextval('comment_edits_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comments ALTER COLUMN id SET DEFAULT nextval('comments_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY feedback ALTER COLUMN id SET DEFAULT nextval('feedback_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY flags ALTER COLUMN id SET DEFAULT nextval('flags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_edits ALTER COLUMN id SET DEFAULT nextval('post_edits_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY posts ALTER COLUMN id SET DEFAULT nextval('posts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY roles ALTER COLUMN id SET DEFAULT nextval('roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY tags ALTER COLUMN id SET DEFAULT nextval('tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: comment_edits; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY comment_edits (id, comment_id, user_id, edit_time, type, content, reason) FROM stdin;
\.


--
-- Name: comment_edits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('comment_edits_id_seq', 1, false);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY comments (id, post_id, content, creation_time, is_edited, is_visible) FROM stdin;
\.


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('comments_id_seq', 1, false);


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY feedback (id, title, email, reason) FROM stdin;
\.


--
-- Name: feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('feedback_id_seq', 1, false);


--
-- Data for Name: flags; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY flags (id, post_id, type, reason) FROM stdin;
\.


--
-- Name: flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('flags_id_seq', 1, false);


--
-- Data for Name: post_edits; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY post_edits (id, post_id, user_id, edit_time, type, title, content, reason, version) FROM stdin;
\.


--
-- Name: post_edits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('post_edits_id_seq', 1, false);


--
-- Data for Name: post_tags; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY post_tags (post_id, tag_id) FROM stdin;
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY posts (id, activist_name, activist_start_date, activist_end_date, content, author_name, author_email, author_website, creation_time, is_edited, is_visible, version) FROM stdin;
\.


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('posts_id_seq', 1, false);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY roles (id, name, "default", permissions) FROM stdin;
\.


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('roles_id_seq', 1, false);


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY tags (id, name) FROM stdin;
\.


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('tags_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sgong
--

COPY users (id, password_hash, first_name, last_name, email, phone, role_id, confirmed, site, is_subscribed) FROM stdin;
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgong
--

SELECT pg_catalog.setval('users_id_seq', 1, false);


--
-- Name: comment_edits_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comment_edits
    ADD CONSTRAINT comment_edits_pkey PRIMARY KEY (id);


--
-- Name: comments_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: flags_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY flags
    ADD CONSTRAINT flags_pkey PRIMARY KEY (id);


--
-- Name: post_edits_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_edits
    ADD CONSTRAINT post_edits_pkey PRIMARY KEY (id);


--
-- Name: post_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_tags
    ADD CONSTRAINT post_tags_pkey PRIMARY KEY (post_id, tag_id);


--
-- Name: posts_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: roles_name_key; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: tags_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_roles_default; Type: INDEX; Schema: public; Owner: sgong
--

CREATE INDEX ix_roles_default ON roles USING btree ("default");


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: sgong
--

CREATE UNIQUE INDEX ix_users_email ON users USING btree (email);


--
-- Name: comment_edits_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comment_edits
    ADD CONSTRAINT comment_edits_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES comments(id);


--
-- Name: comment_edits_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comment_edits
    ADD CONSTRAINT comment_edits_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: flags_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY flags
    ADD CONSTRAINT flags_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: post_edits_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_edits
    ADD CONSTRAINT post_edits_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: post_edits_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_edits
    ADD CONSTRAINT post_edits_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: post_tags_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_tags
    ADD CONSTRAINT post_tags_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: post_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY post_tags
    ADD CONSTRAINT post_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES tags(id);


--
-- Name: users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sgong
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES roles(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: sgong
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM sgong;
GRANT ALL ON SCHEMA public TO sgong;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

