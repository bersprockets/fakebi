drop database if exists prices cascade;

create database if not exists prices;
use prices;

create or replace temp view sec_external_vw (sec_external_id string, country_id bigint, sec_id bigint, sec_external_id_type_id bigint, start_dt date, end_dt date) using json options (path '${HOME}/testbed/price_test_data/sec_external.json');

create table sec_external using orc as select * from sec_external_vw;

create or replace temp view sec_external_id_type_vw (sec_external_id_type_id bigint, country_id bigint, name string) using json options (path '${HOME}/testbed/price_test_data/sec_external_id_type.json');

create table sec_external_id_type using orc as select * from sec_external_id_type_vw;

create or replace temp view sec_vw (sec_id bigint, country_id bigint, name string) using json options (path '${HOME}/testbed/price_test_data/sec.json');

create table sec using orc as select * from sec_vw;

create or replace temp view sec_price_type_vw (sec_price_type_id bigint, sec_price_type_code string) using json options (path '${HOME}/testbed/price_test_data/sec_price_type.json');

create table sec_price_type using orc as select * from sec_price_type_vw;

create or replace temp view exchange_vw (exchange_id bigint, exchange_code string, country_id bigint) using json options (path '${HOME}/testbed/price_test_data/exchange.json');

create table exchange using orc as select * from exchange_vw;


create or replace temp view country_vw (country_id bigint, country_code string) using json options (path '${HOME}/testbed/price_test_data/country.json');

create table country using orc as select * from country_vw;

create table feed_precedence (feed_id bigint, precedence bigint) using orc;
insert into feed_precedence
select * from values
(2, 1),
(1, 2),
(0, 100);

create table sec_price
(
  sec_id bigint,
  exchange_id bigint,
  sec_price_type_id bigint,
  price decimal(32,9),
  price_dt date,
  feed_id bigint
)
using parquet
partitioned by (price_dt, feed_id);

create table sec_price_last
(
  sec_id bigint,
  exchange_id bigint,
  sec_price_type_id bigint,
  price decimal(32,9),
  price_dt date,
  feed_id bigint,
  data_dt date
) using parquet
partitioned by (data_dt);

create table sec_close_price_diff
(
  sec_id bigint,
  exchange_id bigint,
  prev_price decimal(32,9),
  prev_price_dt date,
  price decimal(32,9),
  price_dt date,
  perc_diff double,
  data_dt date,
  feed_id bigint
)
using parquet
partitioned by (data_dt, feed_id);
