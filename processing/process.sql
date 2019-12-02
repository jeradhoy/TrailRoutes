DROP TABLE junctions;
DROP TABLE junct_trail;
DROP TABLE trail_junct_rel;

-- Create unique junctions table
CREATE TABLE junctions AS
SELECT DISTINCT ON (ST_X(geom), ST_Y(geom)) geom FROM endpoints;
ALTER TABLE junctions ADD COLUMN junct_id SERIAL PRIMARY KEY;


-- Create join table for junctions and trails
-- CREATE TABLE junct_trail AS
-- SELECT id as trail_id, junct_id FROM endpoints
-- LEFT JOIN junctions
-- ON ST_X(endpoints.geom) = ST_X(junctions.geom) and ST_Y(endpoints.geom) = ST_Y(junctions.geom);


-- Combine trails and junctions to get to-from points in trail dataset
CREATE TABLE trail_junct_rel AS
WITH junct_trail AS (
    SELECT id as trail_id, junct_id FROM endpoints
    LEFT JOIN junctions
    ON ST_X(endpoints.geom) = ST_X(junctions.geom) and ST_Y(endpoints.geom) = ST_Y(junctions.geom)
),
junct_split as (
    SELECT trail_id,
    min(junct_id) AS junct1,
    max(junct_id) AS junct2
    FROM junct_trail
    GROUP BY trail_id
)
SELECT name, trailnumbe, id::INTEGER, length_mi, junct1, junct2, geom FROM trails
LEFT JOIN junct_split ON junct_split.trail_id = trails.id;


DROP TABLE endpoints;
DROP TABLE trails;

-- Only relevant tables are 'trail_junct_rel' and 'junctions'

-- Dump trail relationships to CSV
-- COPY (SELECT id, length_mi, junct1, junct2 FROM trail_junct_rel) TO '/tmp/trail_relationship.csv' WITH CSV header;

-- Dump trail junctions to csv
-- COPY (SELECT junct_id FROM junctions) TO '/tmp/junctions.csv' WITH CSV header;