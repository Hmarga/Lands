from db_module import create_sqlite_database, create_table, table_definitions, insert_csv_to_table
from faosts import lands_inquire_set, list_to_csv
import timeit
import os


if __name__ == '__main__':
    # Call the function to create the database
    db_folder = 'databases'
    db_name = 'faostat.db'

    lands_inquire_set()
    # Create the DB
    create_sqlite_database(db_folder, db_name)

   # Extract the data using faostat library
    file_path = ['data/area.csv', 'data/population.csv']
    table_name = [fp.split('/')[1].split('.csv') for fp in file_path]
    #table_name = file_path.split('/')[1].split('.csv')[0]

    # for fp in file_path:
    #     if not os.path.exists(fp):
    #         #lands_inquire_set()
    #         list_to_csv(lands_inquire_set(), fp)
    
#     # Create the tables
#     table_info = table_definitions(file_path)
#     create_table(db_folder, db_name, table_info)
#     insert_csv_to_table(db_folder, db_name, table_name, file_path)

# # elapsed_time = timeit.timeit(list_to_csv(lands_inquire_set, filename), number=1)
# # print("----> Average execution time:", elapsed_time, "seconds")