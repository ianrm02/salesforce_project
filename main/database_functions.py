import pg8000
import time
import csv
from config import DBNAME, USER, PASSWORD, HOST

class DatabaseManager:
    def __init__(self):
        """
        TODO: add comment block
        """
        try:
            self.conn = pg8000.connect(
                database=DBNAME,
                user=USER,
                password=PASSWORD,
                host=HOST
            )
            self.cur = self.conn.cursor()
            self.LAST_ID = 1
        except Exception as e:
            raise Exception(f"Failed to connect to the database: {e}")
    
    def __del__(self):
        if hasattr(self, 'cur') and self.cur is not None:
            self.cur.close()
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()

    def insert_address(self, address, state, country):
        try:
            insert_query = "INSERT INTO Addresses (Address, State, Country) VALUES (%s, %s, %s)"
            self.cur.execute(insert_query, (address, state, country))
            self.conn.commit()
            
        except Exception as e:
            print("An error occurred:", e)

    def delete_address(self, condition):
        try:
            delete_query = f"DELETE FROM Addresses WHERE {condition};"
            self.cur.execute(delete_query)
            self.conn.commit()
            
            print("Deleted successfully")

        except Exception as e:
            print(f"An error occurred: {e}")

    def re_id_database(self):
        """
        TODO: add comment block
        """        
        try:
            self.cur.execute("""
                CREATE TEMP TABLE temp_ids AS
                SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id
                FROM Addresses;
            """)
            
            self.cur.execute("""
                UPDATE Addresses
                SET id = temp_ids.new_id
                FROM temp_ids
                WHERE Addresses.id = temp_ids.id;
            """)
            
            self.cur.execute("DROP TABLE temp_ids;")
            
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(f"An error occurred: {e}")

    def get_next_n(self, n):
        """
        TODO: add comment block
        """
        results = []

        count = 0

        for i in range(self.LAST_ID, self.LAST_ID+n):
            self.cur.execute("SELECT address, country, state FROM Addresses WHERE id=%s;", (i,))
            result = self.cur.fetchone()
            if result is None:
                break
            results.append(result)
            count += 1
        
        self.LAST_ID += count

        return results

    def get_db_size(self):
        """
        TODO: add comment block
        """
        try:
            self.cur.execute("SELECT COUNT(*) FROM Addresses;")
            size = self.cur.fetchall()[0][0]
            return size

        except Exception as e:
            print(f"An error occurred: {e}")

    def drop_all_tables(self):
        self.cur.execute("DROP TABLE IF EXISTS Mappings;")
        self.cur.execute("DROP TABLE IF EXISTS Changes;")
        self.cur.execute("DROP TABLE IF EXISTS Addresses;")
        self.conn.commit()

    def create_address_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Addresses;")
        self.cur.execute("""
        CREATE TABLE Addresses (
        ID SERIAL PRIMARY KEY,
        Address VARCHAR(255),
        State VARCHAR(100),
        Country VARCHAR(100)
        );""")
        self.conn.commit()

    def create_change_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Changes;")
        self.cur.execute("""
        CREATE TABLE Changes (
        ChangeID SERIAL PRIMARY KEY,
        Type CHAR(1),
        Old VARCHAR(100),
        New VARCHAR(100)
        );""")
        self.conn.commit()

    def create_mapping_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Mappings;")
        self.cur.execute("""
        CREATE TABLE Mappings (
        ID INT,
        ChangeID INT,
        FOREIGN KEY (ID) REFERENCES Addresses(ID),
        FOREIGN KEY (ChangeID) REFERENCES Changes(ChangeID)
        );""")
        self.conn.commit()

    def setup_database(self):
        """
        TODO: add comment block
        """
        self.drop_all_tables()
        self.create_address_table()
        self.create_change_table()
        self.create_mapping_table()

    def upload_n_entries(self, n):
        """
        TODO: add comment block
        """
        address = 1000
        state = ["TX", "CT", "Buenos Aires", "Bahumbug"]
        country = ["United States", "Merica", "Arg", "Iran"]
        one_twentieth = n // 20

        for i in range(n):
            self.insert_address(address, state[i % 4], country[i % 4])
            address = ((address + i - 1000) % 9000) + 1000
            if (i % one_twentieth == 0):
                print(i)

    def upload_csv_entries(self, filename):
        """
        TODO: add comment block
        """
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
                self.cur.execute(sql, (address, country, state))

            self.conn.commit()
