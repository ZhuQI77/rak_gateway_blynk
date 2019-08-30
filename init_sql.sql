
CREATE DATABASE rak_blynk WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_GB.UTF-8' LC_CTYPE = 'en_GB.UTF-8';


ALTER DATABASE rak_blynk OWNER TO rak_blynk;

\connect rak_blynk

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: log_node; Type: TABLE; Schema: public; Owner: rak_blynk
--

CREATE TABLE public.log_node (
    log_id integer NOT NULL,
    dev_eui character(16) NOT NULL,
    create_at timestamp with time zone NOT NULL,
    humidity integer NOT NULL,
    temperature integer NOT NULL
);


ALTER TABLE public.log_node OWNER TO rak_blynk;

--
-- Name: log_node_log_id_seq; Type: SEQUENCE; Schema: public; Owner: rak_blynk
--

CREATE SEQUENCE public.log_node_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.log_node_log_id_seq OWNER TO rak_blynk;

--
-- Name: log_node_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rak_blynk
--

ALTER SEQUENCE public.log_node_log_id_seq OWNED BY public.log_node.log_id;


--
-- Name: log_node log_id; Type: DEFAULT; Schema: public; Owner: rak_blynk
--

ALTER TABLE ONLY public.log_node ALTER COLUMN log_id SET DEFAULT nextval('public.log_node_log_id_seq'::regclass);


ALTER TABLE ONLY public.log_node
    ADD CONSTRAINT log_node_pkey PRIMARY KEY (log_id);


--
-- Name: log_node_dev_eui_idx; Type: INDEX; Schema: public; Owner: rak_blynk
--

CREATE INDEX log_node_dev_eui_idx ON public.log_node USING btree (dev_eui);


--
-- Name: log_node_dev_eui_log_id_idx; Type: INDEX; Schema: public; Owner: rak_blynk
--

CREATE INDEX log_node_dev_eui_log_id_idx ON public.log_node USING btree (dev_eui, log_id);