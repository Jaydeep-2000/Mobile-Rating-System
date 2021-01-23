import MySQLdb
import MySQLdb.cursors
import json


# reading parameters from config.json
with open ("config.json", "r") as f:
    params = json.load(f)["params"]

# fuction to create connection to database
def connection():
    conn = MySQLdb.connect(host = params["local_host"],
                           user = params["local_user"],
                           passwd = params["local_password"],
                           db = params["local_database"],
                           cursorclass=MySQLdb.cursors.DictCursor,
                           port = 3308)
    cur = conn.cursor()

    return cur, conn