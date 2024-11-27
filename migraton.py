from config.database import create_or_replace_database
from table.table import create_g2g_tables
from dummy.data import generate_dummy_data_with_redis


def main(): 
    create_or_replace_database()
    create_g2g_tables()
    generate_dummy_data_with_redis()



if __name__ == "__main__":
    main()