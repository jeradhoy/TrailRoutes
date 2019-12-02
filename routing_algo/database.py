import psycopg2

# Change user who can access database
#conn = psycopg2.connect(dbname="trailDb", user="postgres", host="localhost", password="meow")

def get_trails(conn,junct_id,distance):
    cur = conn.cursor()

    stmt = """
    SELECT t.id, t.length_mi, t.junct1, t.junct2
        FROM junctions as j, trail_junct_rel AS t
        WHERE j.junct_id = %s AND
        ST_DWithin(t.geom, j.geom, %s);
    """

    cur.execute(stmt, (junct_id, distance))
    trails = cur.fetchall()
    cur.close()

    return(trails)
