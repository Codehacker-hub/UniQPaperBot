import sqlite3

def create_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('pdf_files.db')
        cursor = conn.cursor()

        # Drop the existing table if it exists
        cursor.execute('DROP TABLE IF EXISTS files')

        # Create a table to store PDF file information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stream TEXT NOT NULL,
                semester TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        print("Database and table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Run the function to create the database
create_database()
