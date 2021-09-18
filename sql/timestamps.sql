-- "Key" relation for 6NF data architecture
CREATE OR REPLACE timestamps (
    id  SERIAL  PRIMARY KEY,
    val INT     UNIQUE
);
