import pg8000
import time
import csv
from config import DBNAME, USER, PASSWORD, HOST

class DatabaseManager:
    def __init__(self):
        """
        constructor for DB manager
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
        re index all id values in the address table
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
        get next n results from the , based on a static id variable
        """
        results = []

        count = 0

        for i in range(self.LAST_ID, self.LAST_ID+n):
            self.cur.execute("SELECT * FROM Addresses WHERE id=%s;", (i,))
            result = self.cur.fetchone()
            if result is None:
                break
            results.append(result)
            count += 1
        
        self.LAST_ID += count

        return results

    def get_db_size(self):
        """
        get database size
        """
        try:
            self.cur.execute("SELECT COUNT(*) FROM Addresses;")
            size = self.cur.fetchall()[0][0]
            return size

        except Exception as e:
            print(f"An error occurred: {e}")

    def drop_all_tables(self):
        self.cur.execute("DROP TABLE IF EXISTS AddressChanges;")
        self.cur.execute("DROP TABLE IF EXISTS StateChanges;")
        self.cur.execute("DROP TABLE IF EXISTS CountryChanges;")
        self.cur.execute("DROP TABLE IF EXISTS Addresses;")
        self.conn.commit()

    def address_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Addresses;")
        self.cur.execute("""
        CREATE TABLE Addresses (
        ID SERIAL PRIMARY KEY,
        Address VARCHAR(255),
        State VARCHAR(100),
        Country VARCHAR(100)
        );""")
        self.conn.commit()

    def country_changes_table(self):
        self.cur.execute("DROP TABLE IF EXISTS CountryChanges;")
        self.cur.execute("""
        CREATE TABLE CountryChanges (
        OldCountry VARCHAR(100),
        NewCountry CHAR(2),
        Occurrences INT,
        Confidence SMALLINT
        );""")
        self.conn.commit()

    def state_changes_table(self):
        self.cur.execute("DROP TABLE IF EXISTS StateChanges;")
        self.cur.execute("""
        CREATE TABLE StateChanges (
        StateChangeID SERIAL PRIMARY KEY,
        NewCountry CHAR(2),
        OldState VARCHAR(100),
        NewState CHAR(3),
        Occurrences INT,
        Confidence SMALLINT
        );""")
        self.conn.commit()

    def address_changes_table(self):
        self.cur.execute("DROP TABLE IF EXISTS AddressChanges;")
        self.cur.execute("""
        CREATE TABLE AddressChanges (
        ID INT REFERENCES Addresses(ID),
        Address VARCHAR(255)
        );""")
        self.conn.commit()

    def setup_default_database(self):
        """
        sets default/expected db shape
        """
        self.drop_all_tables()
        self.address_table()
        self.upload_csv_entries("./data/377_items.txt")
    
    def setup_database_extension(self):
        self.country_changes_table()
        self.state_changes_table()
        self.address_changes_table()

    def upload_n_entries(self, n):
        """
        upload n random entries to the database
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
        upload csv entries to the database
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
    
    def store_temp_values(self, values):
        """
        Pass in a tuple that is 10 long with values for NewCo, ConfCo, NewSt, ConfSt, id, Addr, OldSt, and OldCo

        The order is not important, I can easily fix that in this function
        """
        NewCo, ConfCo, NewSt, ConfSt, iD, Addr, OldSt, OldCo = values
        OccCo = self.get_freq('C', OldCo)
        OccSt = self.get_freq('S', OldSt)
        try:
            # Country table
            if (ConfCo != 0):
                # Check for duplicate in CountryChanges
                check_query = "SELECT COUNT(*) FROM CountryChanges WHERE OldCountry = %s AND NewCountry = %s"
                self.cur.execute(check_query, (OldCo, NewCo))
                if self.cur.fetchone()[0] == 0:
                    insert_query = "INSERT INTO CountryChanges (OldCountry, NewCountry, Occurrences, Confidence) VALUES (%s, %s, %s, %s)"
                    self.cur.execute(insert_query, (OldCo, NewCo, OccCo, ConfCo))
                    self.conn.commit()
            # state table
            if (ConfSt != 0):
                #TODO: there might be an error here, if the None type being pushed doesn't automatically convert to Null
                # Check for duplicate in StateChanges
                check_query = "SELECT COUNT(*) FROM StateChanges WHERE NewCountry = %s AND OldState = %s AND NewState = %s"
                self.cur.execute(check_query, (NewCo, OldSt, NewSt))
                if self.cur.fetchone()[0] == 0:
                    insert_query = "INSERT INTO StateChanges (NewCountry, OldState, NewState, Occurrences, Confidence) VALUES (%s, %s, %s, %s, %s)"
                    self.cur.execute(insert_query, (NewCo, OldSt, NewSt, OccSt, ConfSt))
                    self.conn.commit()
            # address table
            if (ConfSt == 0 and ConfCo == 0):
            # Check for duplicate in AddressChanges
                check_query = "SELECT COUNT(*) FROM AddressChanges WHERE ID = %s AND Address = %s"
                self.cur.execute(check_query, (iD, Addr))
                if self.cur.fetchone()[0] == 0:
                    insert_query = "INSERT INTO AddressChanges (ID, Address) VALUES (%s, %s)"
                    self.cur.execute(insert_query, (iD, Addr))
                    self.conn.commit()
                
        except Exception as e:
            print("An error occurred:", e)

    def get_freq(self, appliesTo, value):
        """
        Pass in a char for 'type' ('C' / 'A' / 'S') and a string for 'value'

        This function will then find the number of occurences of that string in the customer database
        """
        if (appliesTo == 'C'):
            try:
                self.cur.execute("SELECT COUNT(*) FROM Addresses WHERE country=%s;", (value, ))
                size = self.cur.fetchall()[0][0]
                return size
            
            except Exception as e:
                print(f"An error occurred: {e}")
        elif (appliesTo == 'S'):
            try:
                self.cur.execute("SELECT COUNT(*) FROM Addresses WHERE state=%s;", (value, ))
                size = self.cur.fetchall()[0][0]
                return size
            
            except Exception as e:
                print(f"An error occurred: {e}")
        elif (appliesTo == 'A'):
            try:
                self.cur.execute("SELECT COUNT(*) FROM Addresses WHERE address=%s;", (value, ))
                size = self.cur.fetchall()[0][0]
                return size
            
            except Exception as e:
                print(f"An error occurred: {e}")
        elif (appliesTo == 'O'):
            pass
        else:
            print("Please enter a valid type \'C\', \'A\', or \'S\'")
            return 0

    #TODO
    def search_db(self, address, state, country):
        # if only one value passed in
        # then return
        none_count = sum(val is None for val in [address, state, country])
        if (none_count >= 2):
            return "Error"

        match (address, state, country):
            # else if state and country
            # search state and country
            case(None, _, _):
                pass
            # else if address and country
            # search address and country
            case(_, None, _):
                pass
            # else if address and state
            # search address and state
            case(_, _, None):
                pass
            # else if all
            # search all
            case (_, _, _):
                pass

    #TODO
    def get_all_from_table(table_name):
        try:
            pass
            #self.cur.execute("SELECT * FROM %s;", (table_name, ))
            #self.
        except Exception as e:
            print("An error occurred:", e)

def test_setup():
    tester = DatabaseManager()
    tester.setup_default_database()
    tester.setup_database_extension()
    print(tester.get_db_size())
    print(tester.get_freq('C', 'IN'))
    tester.insert_address("1234 Taj Mahal Ln.", "New Dehli", "Indania")
    tester.store_temp_values(("IN", 3, "ND", 5, 378, "1234 Taj Mahal Ln.", "New Dehli", "Indania"))
    tester.store_temp_values(("IN", 3, "ND", 5, 378, "1234 Taj Mahal Ln.", "New Dehli", "Indania"))
    tester.store_temp_values(("IN", 3, "ND", 5, 378, "1234 Taj Mahal Ln.", "New Dehli", "Indania"))
    tester.insert_address("2107 Very Cool Rd.", "Texas", "USofAmerica")
    tester.store_temp_values(("UA", 100, None, 0, 362, "kosmonavtov4a, Odessa", "", "Ukraina"))

#test_setup()

sample = ("UA", 100, None, 0, 362, "kosmonavtov4a, Odessa", "", "Ukraina")

for item in sample:
    print(f"{item}: {type(item)}")

    """UA: <class 'str'>
100: <class 'int'>
None: <class 'NoneType'>
0: <class 'int'>
362: <class 'int'>
kosmonavtov4a, Odessa: <class 'str'>
: <class 'str'>
Ukraina: <class 'str'>
"""