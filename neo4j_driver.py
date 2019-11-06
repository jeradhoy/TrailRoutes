from neo4j import GraphDatabase
from typing import *

class TrailGraphDb:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def clear_database(self):
        with self._driver.session() as session:
            return session.run(
                "MATCH (n) "
                "DETACH DELETE n").data()

    def load_junctions(self):
        with self._driver.session() as session:
            return session.run(
                "USING PERIODIC COMMIT "
                "LOAD CSV WITH HEADERS FROM 'file:/junctions.csv' AS row "
                "CREATE (:Junction {id: row.junct_id})").data()

    def load_trail_relationships(self):
        with self._driver.session() as session:
            return session.run(
                "USING PERIODIC COMMIT "
                "LOAD CSV WITH HEADERS FROM 'file:/trailRelationship.csv' AS row "
                "MATCH (startjunct:Junction {id: row.junct1}) "
                "MATCH (endjunct:Junction {id: row.junct2}) "
                "MERGE (startjunct)-[:TRAIL {len: toFloat(row.length_mi), id: row.id}]->(endjunct)").data()


    def get_kshortest_paths(self, node1, node2, k=10) -> List[Dict]:
        with self._driver.session() as session:
            return session.run(
                    "MATCH (start:Junction {id:$startNode}), (end:Junction{id:$endNode}) "
                    "CALL algo.kShortestPaths.stream(start, end, $k, 'len', {path:true}) "
                    "YIELD nodeIds, costs, path "
                    "RETURN [node in algo.getNodesById(nodeIds) | node.id] AS nodes, "
                    "path, "
                    "costs, "
                    "reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost", startNode=node1, endNode=node2, k=k).data()

def process_result_path(result_path):
    path = list(zip(result_path["nodes"][0:-1], result_path["nodes"][1:], result_path["costs"]))
    return {"Total Miles:": result_path["totalCost"], "Path": path}

def main():

    db = TrailGraphDb("bolt://localhost:7687", "neo4j", "hineo4j")
    db.clear_database()
    db.load_junctions()
    db.load_trail_relationships()

    result = db.get_kshortest_paths("6228", "6230", k=10)
    [process_result_path(path) for path in result]

    result2 = db.get_kshortest_paths("3729", "3441", k=10)
    [process_result_path(path) for path in result2]



if __name__=="__main__":
    main()