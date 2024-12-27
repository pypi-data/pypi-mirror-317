import os

from neomodel import config
from sqlalchemy import create_engine

if (neo4j_url := os.getenv("NEO4J_URL")) is None:
    raise ValueError("You have not set neo4j database url using environment `NEO4J_URL`.")
else:
    config.DATABASE_URL = neo4j_url
    # HACK: server may kill idle connection, to avoid being hung for
    # a long time, we kill the connection first, the max lifetime
    # should be less then 4 mins (240 seconds)
    config.MAX_CONNECTION_LIFETIME = 200

if (mysql_url := os.getenv("MYSQL_URL")) is None:
    raise ValueError("You have to set mysql database url using environment `MYSQL_URL`.")
else:
    engine = create_engine(mysql_url, pool_pre_ping=True, pool_recycle=3600)
