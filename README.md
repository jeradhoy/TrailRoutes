# README

    National trail data from: https://catalog.data.gov/dataset/usgs-national-transportation-dataset-ntd-downloadable-data-collectionde7d2

    https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Tran/Shape/
    https://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/Shape/TRAN_12_Florida_GU_STATEORTERRITORY.zip

    wget -r --no-parent http://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/Shape/

    wget -r --no-parent "http://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/Shape/"



1. Process trail data in qgis to get split trails and endpoints
2. Load into Postgres


# Write possible pg_routing extension to include our trail algorithm

Typescript/React wrapper over mapbox map, with left bar for trail possibilities, and a 2-sided slider for selecting length

Do trail to trail or loop mode.

For david's thing: select multiple start points ( or none) and multiple destinations (campsites) and enumerate the possibilities.


# gis_processing

# Write script to download each state from placeif possible

1. Reproject (to 3857)
1. Drop Fields
1. Dissolve
2. merge lines
3. split with lines
4. Add unique (autoincrement) index
4. extract specfic vertices (0, -1)
5. Calculate length

# Interesting that OnX doesn't merge lines within same reach, making arbitrary points along trail

# First need to join all lines (by endpoints touching)
Dissolve by Name and trail number

## Split lines at intersections
Processing toolbox -> QGIS Geoalgorithms -> Vector Overlay tools -> Split lines by lines

{ 'INPUT' : '/home/meow/Classes/Databases/Polyglot/Shape/Trans_TrailSegment.shp', 'LINES' : '/home/meow/Classes/Databases/Polyglot/Shape/Trans_TrailSegment.shp', 'OUTPUT' : 'memory:' }


## Generate intersection points and/or endpoints
processing.runalg('qgis:lineintersections', input_a, input_b, field_a, field_b, output)

Extract Specific Vertices
0,-1

## Merge those points (probably)

# I need to end up with connected lines between trail junctions and trail ends with points at trail junctions and trail ends. If I can preserve trail name and number, (and maybe even USFS designations), that would be ideal, but I don't need it for this prototype.



# Neo4j graph algorithms install: had to move jar to /var/lib/neo4j/plugins and add:

```
dbms.security.procedures.unrestricted=algo.*,apoc.*
```
to
/etc/neo4j/neo4j.conf


# Probably need web server in the middle to serve mapbox tiles:
Tegola and Martin seem like two good ones:
https://tegola.io/tutorials/tegola-with-mapbox/
https://github.com/urbica/martin

Martin seems to be under more active development
