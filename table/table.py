import psycopg2


def create_g2g_tables():
    conn = psycopg2.connect(
        dbname="g2g_offer_management",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    cursor.execute("DROP TABLE IF EXISTS offer;")
    cursor.execute("DROP TABLE IF EXISTS seller;")
    print("Existing tables dropped (if they existed).")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seller (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Table 'seller' created successfully.")

    cursor.execute("""
    CREATE OR REPLACE FUNCTION enforce_lowercase_email()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.email = LOWER(NEW.email);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER lowercase_email_trigger
    BEFORE INSERT OR UPDATE ON seller
    FOR EACH ROW
    EXECUTE FUNCTION enforce_lowercase_email();
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offer (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        seller_id UUID NOT NULL REFERENCES seller(id) ON DELETE CASCADE,
        category VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Table 'offer' created successfully.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables 'seller' and 'offer' created successfully!")


if __name__ == "__main__":
    create_g2g_tables()
