MATCH (n)
DETACH DELETE n;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/junctions.csv" AS row
CREATE (:Junction {id: row.junct_id});

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/trailRelationship.csv" AS row
MATCH (startjunct:Junction {id: row.junct1})
MATCH (endjunct:Junction {id: row.junct2})
MERGE (startjunct)-[:TRAIL {len: toFloat(row.length_mi), id: row.id}]->(endjunct);

// USING PERIODIC COMMIT
// LOAD CSV WITH HEADERS FROM "file:/trailRelationship.csv" AS row
// MATCH (startjunct:Junction {id: row.junct1})
// MATCH (endjunct:Junction {id: row.junct2})
// MERGE (endjunct)-[:TRAIL {len: toFloat(row.length_mi)}]->(endjunct);
//, relationshipQuery:'MATCH (n:Junction)-[t:TRAIL]-(m:Junction) RETURN t.trail_id'

MATCH (start:Junction {id:'6228'}), (end:Junction{id:'6230'})
CALL algo.kShortestPaths.stream(start, end, 10, 'len', {path: true})
YIELD nodeIds, costs, path
RETURN [node in algo.getNodesById(nodeIds) | node.id] AS nodes,
       path,
       costs,
       reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost;

MATCH (start:Junction {id:'6228'})-[t:TRAIL]-(end:Junction{id:'6218'}) RETURN t.trail_id;



MATCH p=()-[r:PATH_0]->() RETURN p LIMIT 25

MATCH (n)
RETURN n;