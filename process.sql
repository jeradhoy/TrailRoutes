DROP TABLE junctions;
DROP TABLE junct_trail;

-- Create unique junctions table
CREATE TABLE junctions AS
SELECT DISTINCT ON (ST_X(geom), ST_Y(geom)) geom FROM endpoints;
ALTER TABLE junctions ADD COLUMN junct_id SERIAL PRIMARY KEY;

-- Create join table for junctions and trails
CREATE TABLE junct_trail AS
SELECT id as trail_id, junct_id FROM endpoints
LEFT JOIN junctions
ON ST_X(endpoints.geom) = ST_X(junctions.geom) and ST_Y(endpoints.geom) = ST_Y(junctions.geom);

DROP TABLE junct_rel;

CREATE TABLE junct_rel AS

WITH junct_split as (
    SELECT trail_id,
    min(junct_id) AS junct1,
    max(junct_id) AS junct2
    FROM junct_trail
    GROUP BY trail_id
)
SELECT name, trailnumbe, id::INTEGER, length_mi, junct1, junct2, geom FROM trails
LEFT JOIN junct_split ON junct_split.trail_id = trails.id;


select id from junct_rel limit 5;
6228
6230
SELECT id, junct1 as source, junct2 as target, length_mi as cost from junct_rel;

WITH ksp AS (
    SELECT  * FROM  pgr_KSP(
            'SELECT id, junct1 as source, junct2 as target, length_mi as cost from junct_rel',
            6228, 6230, 3, 
            directed := FALSE
        )
)
SELECT * FROM trails 
RIGHT JOIN ksp.edge = trails.trail_id WHERE ksp.path_id = 1;

SELECT id from junct_rel;

SELECT * FROM  pgr_KSP(
        'SELECT id, junct1 as source, junct2 as target, length_mi as cost from junct_rel',
        5488, 5487, 10, 
        directed := FALSE
    )

WITH ksp AS (
    SELECT  seq, edge FROM  pgr_KSP(
            'SELECT id, junct1 as source, junct2 as target, length_mi as cost from junct_rel',
            5488, 5487, 10, 
            directed := FALSE
        )
    WHERE path_id = 1
) SELECT * FROM junct_rel RIGHT JOIN ksp ON ksp.edge = junct_rel.id;











-- Dump trail relationships to CSV
COPY (
    WITH junct_split as (
        SELECT trail_id,
        min(junct_id) AS junct1,
        max(junct_id) AS junct2
        FROM junct_trail
        GROUP BY trail_id
    )
    SELECT name, trailnumbe, id, length_mi, junct1, junct2 FROM trails
    LEFT JOIN junct_split ON junct_split.trail_id = trails.id
) TO '/tmp/trailRelationship.csv' WITH CSV header;

-- Dump trail junctions to csv
COPY (SELECT junct_id FROM junctions) TO '/tmp/junctions.csv' WITH CSV header;

-- Need to move to Neo4j folder