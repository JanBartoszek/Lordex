--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.12
-- Dumped by pg_dump version 9.5.12

-- Started on 2018-06-26 13:19:11 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12395)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2209 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 184 (class 1259 OID 24796)
-- Name: answer; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.answer OWNER TO janex;

--
-- TOC entry 183 (class 1259 OID 24794)
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: janex
--

CREATE SEQUENCE public.answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO janex;

--
-- TOC entry 2210 (class 0 OID 0)
-- Dependencies: 183
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: janex
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- TOC entry 186 (class 1259 OID 24805)
-- Name: comment; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


ALTER TABLE public.comment OWNER TO janex;

--
-- TOC entry 185 (class 1259 OID 24803)
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: janex
--

CREATE SEQUENCE public.comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO janex;

--
-- TOC entry 2211 (class 0 OID 0)
-- Dependencies: 185
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: janex
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- TOC entry 182 (class 1259 OID 24787)
-- Name: question; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.question OWNER TO janex;

--
-- TOC entry 181 (class 1259 OID 24785)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: janex
--

CREATE SEQUENCE public.question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO janex;

--
-- TOC entry 2212 (class 0 OID 0)
-- Dependencies: 181
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: janex
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- TOC entry 187 (class 1259 OID 24812)
-- Name: question_tag; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO janex;

--
-- TOC entry 189 (class 1259 OID 24817)
-- Name: tag; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO janex;

--
-- TOC entry 188 (class 1259 OID 24815)
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: janex
--

CREATE SEQUENCE public.tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO janex;

--
-- TOC entry 2213 (class 0 OID 0)
-- Dependencies: 188
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: janex
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- TOC entry 190 (class 1259 OID 24911)
-- Name: user; Type: TABLE; Schema: public; Owner: janex
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    user_name text,
    user_password text,
    registration_time timestamp without time zone
);


ALTER TABLE public."user" OWNER TO janex;

--
-- TOC entry 2051 (class 2604 OID 24799)
-- Name: id; Type: DEFAULT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- TOC entry 2052 (class 2604 OID 24808)
-- Name: id; Type: DEFAULT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- TOC entry 2050 (class 2604 OID 24790)
-- Name: id; Type: DEFAULT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- TOC entry 2053 (class 2604 OID 24820)
-- Name: id; Type: DEFAULT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- TOC entry 2194 (class 0 OID 24796)
-- Dependencies: 184
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: janex
--

INSERT INTO public.answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, NULL);
INSERT INTO public.answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', NULL);
INSERT INTO public.answer VALUES (3, '2018-06-12 11:47:47.988438', 0, 2, 'aaaaaaaaaaaaaaaa', '', NULL);


--
-- TOC entry 2214 (class 0 OID 0)
-- Dependencies: 183
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: janex
--

SELECT pg_catalog.setval('public.answer_id_seq', 2, true);


--
-- TOC entry 2196 (class 0 OID 24805)
-- Dependencies: 186
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: janex
--

INSERT INTO public.comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', NULL, NULL);
INSERT INTO public.comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', NULL, NULL);


--
-- TOC entry 2215 (class 0 OID 0)
-- Dependencies: 185
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: janex
--

SELECT pg_catalog.setval('public.comment_id_seq', 2, true);


--
-- TOC entry 2192 (class 0 OID 24787)
-- Dependencies: 182
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: janex
--

INSERT INTO public.question VALUES (1, '2017-04-29 09:19:00', 30, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', NULL);
INSERT INTO public.question VALUES (5, '2018-06-25 10:30:26', 5, 0, 'asdaaaaaaaaaaaa', 'asdasdaaaaaaaaaaaaa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1200px-Git-logo.svg.png', NULL);
INSERT INTO public.question VALUES (4, '2018-06-14 10:46:31', 25, 0, 'aaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', '', NULL);
INSERT INTO public.question VALUES (0, '2017-04-28 08:29:00', 37, 8, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, NULL);
INSERT INTO public.question VALUES (2, '2017-05-01 10:41:00', 1387, 58, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, NULL);


--
-- TOC entry 2216 (class 0 OID 0)
-- Dependencies: 181
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: janex
--

SELECT pg_catalog.setval('public.question_id_seq', 2, true);


--
-- TOC entry 2197 (class 0 OID 24812)
-- Dependencies: 187
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: janex
--

INSERT INTO public.question_tag VALUES (0, 1);
INSERT INTO public.question_tag VALUES (1, 3);
INSERT INTO public.question_tag VALUES (2, 3);
INSERT INTO public.question_tag VALUES (4, 4);
INSERT INTO public.question_tag VALUES (4, 3);


--
-- TOC entry 2199 (class 0 OID 24817)
-- Dependencies: 189
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: janex
--

INSERT INTO public.tag VALUES (1, 'python');
INSERT INTO public.tag VALUES (2, 'sql');
INSERT INTO public.tag VALUES (3, 'css');
INSERT INTO public.tag VALUES (4, 'GIT');


--
-- TOC entry 2217 (class 0 OID 0)
-- Dependencies: 188
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: janex
--

SELECT pg_catalog.setval('public.tag_id_seq', 4, true);


--
-- TOC entry 2200 (class 0 OID 24911)
-- Dependencies: 190
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: janex
--



--
-- TOC entry 2059 (class 2606 OID 24825)
-- Name: pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- TOC entry 2062 (class 2606 OID 24827)
-- Name: pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- TOC entry 2056 (class 2606 OID 24829)
-- Name: pk_question_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- TOC entry 2064 (class 2606 OID 24831)
-- Name: pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- TOC entry 2066 (class 2606 OID 24833)
-- Name: pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- TOC entry 2068 (class 2606 OID 24918)
-- Name: user_id; Type: CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_id PRIMARY KEY (user_id);


--
-- TOC entry 2060 (class 1259 OID 24935)
-- Name: fki_comment_user_id; Type: INDEX; Schema: public; Owner: janex
--

CREATE INDEX fki_comment_user_id ON public.comment USING btree (user_id);


--
-- TOC entry 2054 (class 1259 OID 24941)
-- Name: fki_question_user_id; Type: INDEX; Schema: public; Owner: janex
--

CREATE INDEX fki_question_user_id ON public.question USING btree (user_id);


--
-- TOC entry 2057 (class 1259 OID 24924)
-- Name: fki_user_id; Type: INDEX; Schema: public; Owner: janex
--

CREATE INDEX fki_user_id ON public.answer USING btree (user_id);


--
-- TOC entry 2074 (class 2606 OID 24930)
-- Name: comment_user_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- TOC entry 2072 (class 2606 OID 24834)
-- Name: fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- TOC entry 2070 (class 2606 OID 24839)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2075 (class 2606 OID 24844)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2073 (class 2606 OID 24849)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2076 (class 2606 OID 24854)
-- Name: fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- TOC entry 2069 (class 2606 OID 24936)
-- Name: question_user_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_user_id FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- TOC entry 2071 (class 2606 OID 24919)
-- Name: user_id; Type: FK CONSTRAINT; Schema: public; Owner: janex
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- TOC entry 2208 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2018-06-26 13:19:11 CEST

--
-- PostgreSQL database dump complete
--

