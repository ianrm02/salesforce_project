import pg8000
from database_functions import connect_to_db, close_db, upload_csv_to_db, get_next_n

def create_default_table():
    conn, cur = connect_to_db()
    cur.execute("DROP TABLE IF EXISTS Addresses;")
    cur.execute("""
    CREATE TABLE Addresses (
    ID SERIAL PRIMARY KEY,
    Address VARCHAR(255),
    State VARCHAR(100),
    Country VARCHAR(100)
    );""")
    conn.commit()
    close_db(cur, conn)

create_default_table()
upload_csv_to_db('main/377_items.txt')

result = get_next_n(377)
print(len(result))