from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

def run_migration():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Drop the existing conference_requests table
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS conference_requests CASCADE"))
        conn.commit()
    
    # Create the new conference_requests table
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE conference_requests (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                description TEXT,
                link VARCHAR,
                type VARCHAR NOT NULL,
                departement VARCHAR NOT NULL,
                requested_by_id INTEGER REFERENCES users(id),
                status VARCHAR NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()

    # Add language and theme columns to users table
    with engine.connect() as conn:
        # Check if columns exist
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN ('language', 'theme')
        """))
        existing_columns = [row[0] for row in result]
        
        # Add language column if it doesn't exist
        if 'language' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN language VARCHAR DEFAULT 'fr'
            """))
        
        # Add theme column if it doesn't exist
        if 'theme' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN theme VARCHAR DEFAULT 'light'
            """))
        
        conn.commit()

if __name__ == "__main__":
    run_migration()
    print("Migration completed successfully!") 