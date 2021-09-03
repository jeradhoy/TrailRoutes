# [TrailRoutes](http://trailroutes.jerad.co): A running and backpacking trail route finding application

The following writeup was submitted for the graduate level MSU CS class, CSCI 550: Advanced Databases, for our semester project. Here's a [link](https://docs.google.com/presentation/d/1Nafbu3PLJ1HX8OhaLzmBLX5mWZhNjKrHxeWugF80GmE/edit?usp=sharing) to the slides we presented about it.

## Problem Statement

Finding possible routes to run, hike, or backpack on can be complicated and time consuming. To find the distance between two trailheads on a backpacking through-hike or to determine what ways you could run in order to achieve a given distance traditionally takes time looking at maps and adding up the lengths of each trail segment listed. To make this easier, we wanted to create an application that could give you trail route options given inputs of where you want to start and end and your desired distance. That is, from the given trailhead, what point-to-point, out-and-back, and loop routes can be followed to roughly achieve the given maximum distance.

## Overview of Solution
Our application consists of a user-facing website (located at the domain trailroutes.run), that allows a user to view all United States Geological Survey (USGS) trails in the United States. Users select the types of routes they wish to query and a maximum distance. With this information, a set of queries are returned and displayed in the sidebar. A screenshot of the application can be seen below:

## Architecture

The front end is built using HTML, CSS, JavaScript, and the Mapbox GL JS javascript library. Mapbox provides functionality to initialize an interactive map of the world and populate our United States trail data within the interactive map. This frontend is served as static files from the Flask Python library. Also utilizing Flask, a Python REST API is set up on our server allowing for GET requests to be sent from the system’s front end. When trailhead data and a maximum distance is input, a GET request is sent to our backend with this information. From here, our Python script either queries for a cached result from Redis or, failing that, queries our Postgres/PostGIS database and returns a subset of trails within the given distance from our trailhead.

With the subset of trails from Postgres, including information about the trail’s ID, starting and ending nodes, and length, a dictionary representing our trail graph is built. This is then fed into the routing algorithm to retrieve our route result, before being returned to the web application via the REST API.

Data for this was preprocessed in QGIS to produce the desired graph structure and attributes. Notably, each trail was broken up into approximately 0.5 mile increments in order to allow for paths that stop mid-trail. This produces more realistic routes than if nodes were only located at trail junctions. This does, however, cause both a coarseness to the routes that will be found along a given trail, and a proliferation of results returned for a given query. To serve the trail and point data that is plotted directly in our application, this trail data, after being preprocessed, was uploaded to Mapbox Studio, for easy and convenient access from Mapbox GL JS.

## Routing Algorithm

This routing algorithm is written in Python and performs a fairly straightforward extension of Depth First Search (DFS). This is used for both point-to-point searches and out-and-back routes. For out-and-back, we run DFS until it passes a threshold of the maximum distance divided by two. After enumerating these possible paths, we match paths who both have identical endpoints and have the sum of their distances being less than or equal to our distance threshold.

For point-to-point queries, the same DFS search is performed, but from both trailheads up to the distance threshold divided by two. Likewise, path endpoints are matched together and the total lengths are compared to our distance input to yield possible routes. DFS works well here, as opposed to BFS, because we are trying to enumerate all possible paths from one point to another, as opposed to find the shortest routes and simply visiting all nodes. With a max distance parameter, DFS does not fall into the pitfall of going too far and deep down individual paths.

The graph of trails and trail junctions in our system is represented as a dictionary where the keys are trail junctions and the values are the junctions that connect to the key, along with their identifying trail and length information. After generating routes, the results are output to the web application and plotted via Mapbox.

## Caching
In the event that redundant requests for routes are made, we wanted to mitigate the need to repeatedly run our algorithm for similar queries. By utilizing Redis, possible paths are cached with an associated trailhead or trailheads. These paths are cached after being produced from the DFS algorithm. In the case that a requested route falls within the scope (less than or equal to the largest distance queried) of a previous query, the Redis cache can be quickly checked before the algorithm is run.

## Limitations and Future Work
The results are limited to trails we have in the database. There are a quantity of trails which are not contained in our database. This is due to limitations in the quality of the USGS data. For example, no trails are shown in the Tobacco Root Mountains. In the future, we would like to fill in these gaps, likely by gathering data from different agencies or county-level GIS repositories.

The results returned do not include roads or jeep roads. This could be limiting the quality of the results of our queries. In the future, we would like to expand the database to include certain roads and jeep roads within a proximity to trails and trailheads. Additionally, due to the nature of the USGS data, trailheads in close proximity to one another are not modelled as connected. This means potential routes with close starting and ending trailheads (often showing up in the same parking lot), are not shown when querying for loops. They can, however, be found by doing a point-to-point search. In the future, we would like to implement snapping points between trailheads within a deterministic distance while avoiding potential hazards such as rivers and cliffs. This allows for these gaps to be listed as a continuous trail within our database and returned in query results.

Many routes returned are quite similar, and contribute to a large number of results being returned per query. These routes clog the query results making it difficult to parse through a wide variety of trails. Given more time, we would like to limit the number of out-and-back queries in a meaningful way which improves the search results. Perhaps eliminating out-and-back trails which are very closely related could achieve this. This could be done by implementing a similarity metric to group similar routes.

For queries with large distances and/or complex trail networks, the routing algorithm is quite slow. As of now, the route processing algorithm runs in approximately O(n2) time. By this measure, long, complex routes can take upwards of twenty seconds. To combat this, the maximum distance input is limited to fifty miles at most. The limiting procedure is the path-end matching routine. This could be sped up by storing the paths in a dictionary with the key being the endpoint. Then end-matching would consist of only comparing paths within the same key. This has the potential to significantly speed up this part of our algorithm.

Given more time, we would also like to improve some of the styling and functionality of the website. As of now the website is fairly bare bones and not very visually appealing. The design could definitely be improved.

<h2 align="center">Thanks!</h2>


# Random Notes:

National trail data gathered from USGS at: 

https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Tran/Shape/
