import sqlite3
import os
import csv
import chardet

def create_sqlite_database(db_folder, db_name):
    """ create a database connection to an SQLite database """

    db_folder = 'databases'
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    db_path = os.path.join(db_folder, db_name)

    conn = None
    try:
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def table_definitions(source_file):
    '''
    create a list of tuples with the parameters of the columns of the table:
    ('table_name', [
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("column1", "type of object(INT, STR, etc)"),
    ("column2", "type of object(INT, STR, etc)"])
    '''

    with open(source_file, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        table_name = source_file.split('/')[1].split('.csv')[0]
        first_line = next(csv_reader)
        col_type = 'TEXT'
        tdef = [(cname, col_type) for cname in first_line]
        tdef.insert(0, ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"))
        return table_name, tdef


def create_table(db_folder, db_name, table_definitions):
  """Creates tables in a SQLite database.

  Args:
    db_file: The name of the SQLite database file.
    table_definitions: A list of tuples, where each tuple contains the table name 
    and its column definitions.
  """
  db_path = os.path.join(db_folder, db_name)
  conn = sqlite3.connect(db_path)

  table_name = table_definitions[0]
  columns = table_definitions[1]
 
  # Construct the SQL CREATE TABLE statement
  columns_with_types = ', '.join([f'"{col_name}" {col_type}' for col_name, col_type in columns])
  create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"

  # Execute the CREATE TABLE command
  cursor = conn.cursor()
  cursor.execute(create_table_query)
  
  # Commit changes
  conn.commit()
  cursor.close()
  conn.close()


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def insert_csv_to_table(db_folder, db_name, table_name, data_source):
    """
    Insert data from a CSV file into an SQLite table.

    :param table_name: Name of the table
    :param db_folder, db_name: Path to the CSV file
    """
    
    csv_file = data_source
    encoding = detect_encoding(csv_file)

    # Open the CSV file to remove the null characters.
    with open(csv_file, 'rb') as file:
        content = file.read().replace(b'\x00', b'')  # Remove NUL characters
    
    # Decode the cleaned content
    decoded_content = content.decode(encoding)  # Use appropriate encoding
    reader = csv.reader(decoded_content.splitlines())
    columns = next(reader)  # This assumes the first row is the header

    db_path = os.path.join(db_folder, db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build the INSERT query
    insert_query = f"""
        INSERT INTO {table_name} ({", ".join([f'"{col}"' for col in columns])})
        VALUES ({", ".join(["?"] * len(columns))})
        """

    # Insert the CSV data into the SQLite table
    cursor.executemany(insert_query, reader)

    # Commit the changes to the database
    conn.commit()
    print(f"Data from {csv_file} inserted successfully into {table_name}.")
    cursor.close()
    conn.close()
