CREATE DATABASE IF NOT EXISTS db;
\ c db CREATE SCHEMA test_schema;
CREATE TABLE test_schema.ma_table (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100)
);