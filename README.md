# README

## Priorities

Dave's Requirements:
1. Build a user interface
2. Cache partial paths with redis
3. Merge trails for entire US
4. Point-to-point (consider simul BFS)
5. OPTIONAL: Path similarity (if actually an issue) - ferche distance...


---------------------


1. Get initial map UI up and running
2. Plot trails from PostGIS on map (need map tile server)
3. Connect it with python Routing backend
4. Create sidebar to display routing results

If there is time:

5. Implement Redis as a caching layer for partial paths
6. Group similar trail routes with similarity score
7. Implement glacier campsite optimizer...

If we can get a frontend up, at least we will have something to show.

## Implementaion Notes

We could do front end entirely with html/css/javascript/mapboxgl.

Or we could use a javascript framework like React - more time to learn but might be better experience.

We will need a map tile server such as Martin to serve trails and junctions from postgres.

Seperate server will interface with trail routing backend.

# Random Notes:

National trail data from: https://catalog.data.gov/dataset/usgs-national-transportation-dataset-ntd-downloadable-data-collectionde7d2

https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Tran/Shape/
https://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/Shape/TRAN_12_Florida_GU_STATEORTERRITORY.zip

# gis_processing

# GIS Processing Steps

1. Load them all
2. Merge vector layers
1. Reproject (to 3857) (to get proper length calculations...)
1. Drop Fields (Everything except NAME, TRAILNUMBE, SOURCE_ORI, SOURCE_D_1)
1. Dissolve (On trail number and name)
2. merge lines
3. split with lines
3. v.split at 0.5 mile increment
4. Add unique (autoincrement) index (name field "id")
4. extract specfic vertices (0, -1)
5. Calculate length (Field calculator, length_mi) ( $length * 0.000621371)

Save shapefiles
Load into postgres
Process with postgresql
Export from postgres to GEOJSON
Upload to mapbox


# Probably need web server in the middle to serve mapbox tiles:
Tegola and Martin seem like two good ones:
https://tegola.io/tutorials/tegola-with-mapbox/
https://github.com/urbica/martin

Martin seems to be under more active development
