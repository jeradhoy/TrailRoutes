# [TrailRoutes.run](trailroutes.run): A running and backpacking trail route finding application






# Random Notes:

National trail data from: 
https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Tran/Shape/

# GIS Processing Steps

1. Reproject (to 3857) (to get proper length calculations...)
1. Drop Fields (Everything except NAME, TRAILNUMBE, SOURCE_ORI, SOURCE_D_1)
1. Dissolve (On trail number and name)
Need to snap lines together (snapped geometry) (possibley with large enough tolerance to connect bear canyon and spanish creek trailheads... or see if I can have an attribute that signifies sanpped trailheads)
2. merge lines
3. split with lines
3. v.split at 0.5 mile increment
4. Add unique (autoincrement) index (name field "id")
4. extract specfic vertices (0, -1)
5. Calculate length (Field calculator, length_mi) ( $length * 0.000621371)
2. Merge vector layers