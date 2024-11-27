from config.database import create_or_replace_database
from table.table import create_g2g_tables


def main(): 
    create_or_replace_database()
    create_g2g_tables()



if __name__ == "__main__":
    main()