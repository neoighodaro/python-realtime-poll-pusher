import sqlite3, json
from sqlite3 import Error
 
def create_connection(database):
    try:
        conn = sqlite3.connect(database, isolation_level=None, check_same_thread = False)
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        
        return conn
    except Error as e:
        print(e)

def create_table(c):
    sql = """ 
        CREATE TABLE IF NOT EXISTS items (
            id integer PRIMARY KEY,
            name varchar(225) NOT NULL,
            votes integer NOT NULL Default 0
        ); 
    """
    c.execute(sql)

def create_item(c, item):
    sql = ''' INSERT INTO items(name)
              VALUES (?) '''
    c.execute(sql, item)

def update_item(c, item):
    sql = ''' UPDATE items
              SET votes = votes+1 
              WHERE name = ? '''
    c.execute(sql, item)

def select_all_items(c, name):
    sql = ''' SELECT * FROM items '''
    c.execute(sql)
 
    rows = c.fetchall()
    rows.append({'name' : name})
    return json.dumps(rows)
 
def main():
    database = "./pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)

    # create items table
    create_table(conn)
    create_item(conn, ["Go"])
    create_item(conn, ["Python"])
    create_item(conn, ["PHP"])
    create_item(conn, ["Ruby"])
    print("Connection established!")

if __name__ == '__main__':
    main()



