import pg8000
import time
import csv
from config import DBNAME, USER, PASSWORD, HOST

LAST_ID = 1

def connect_to_db():
    conn = pg8000.connect(
        database=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST
    )
    cur = conn.cursor()
    return conn, cur

def close_db(cur: pg8000.Cursor, conn: pg8000.Connection):
    cur.close()
    conn.close()

def insert_address(address, state, country):
    try:
        conn, cur = connect_to_db()
        insert_query = "INSERT INTO Addresses (Address, State, Country) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (address, state, country))
        conn.commit()
        
    except Exception as e:
        print("An error occurred:", e)

    finally:
        if conn:
            close_db(cur, conn)

def delete_address(condition):
    try:
        conn, cur = connect_to_db()
        delete_query = f"DELETE FROM Addresses WHERE {condition};"
        cur.execute(delete_query)
        conn.commit()
        
        print("Deleted successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            close_db(cur, conn)

def re_id_database():
    conn, cur = connect_to_db()
    
    try:
        cur.execute("""
            CREATE TEMP TABLE temp_ids AS
            SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id
            FROM Addresses;
        """)
        
        cur.execute("""
            UPDATE Addresses
            SET id = temp_ids.new_id
            FROM temp_ids
            WHERE Addresses.id = temp_ids.id;
        """)
        
        cur.execute("DROP TABLE temp_ids;")
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    finally:
        if conn:
            close_db(cur, conn)

def get_next_n(n):
    global LAST_ID

    results = []

    conn, cur = connect_to_db()
    count = 0

    for i in range(LAST_ID, LAST_ID+n):
        cur.execute("SELECT * FROM Addresses WHERE id=%s;", (i,))
        result = cur.fetchone()
        if result is None:
            break
        results.append(result)
        count += 1
    
    LAST_ID += count

    close_db(cur, conn)

    return results

def timing_test():
    start_time = time.time()

    conn, cur = connect_to_db()

    cur.execute("SELECT COUNT(*) FROM Addresses;")
    size = cur.fetchall()[0][0]
    print(size)

    for i in range(1, size+1):
        cur.execute("SELECT * FROM Addresses WHERE id=%s;", (i,))

    end_time = time.time()

    print(f"Duration: {end_time - start_time} seconds")

    close_db(cur, conn)

def insert_n_entries(n):
    conn, cur = connect_to_db()
    address = 1000
    state = ["TX", "CT", "Buenos Aires", "Bahumbug"]
    country = ["United States", "Merica", "Arg", "Iran"]
    one_twentieth = n // 20

    for i in range(n):
        insert_address(address, state[i % 4], country[i % 4])
        address = ((address + i - 1000) % 9000) + 1000
        if (i % one_twentieth == 0):
            print(i)

    close_db(cur, conn)

def upload_csv_to_db(filename):
    conn, cur = connect_to_db()

    with open(filename, newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            address = row[0]
            country = row[1]
            state = row[2]

            sql = """
            INSERT INTO Addresses (address, country, state)
            VALUES (%s, %s, %s)
            """
            cur.execute(sql, (address, country, state))

        conn.commit()

    close_db(cur, conn)


def get_db_size():
    try:
        conn, cur = connect_to_db()

        cur.execute("SELECT COUNT(*) FROM Addresses;")
        size = cur.fetchall()[0][0]
        close_db(cur, conn)
        
        return size

    except Exception as e:
        print(f"An error occurred: {e}")

#insert_n_entries(1_000_000)
re_id_database()