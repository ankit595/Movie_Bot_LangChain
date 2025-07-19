import pandas as pd
import sqlite3

try:
    # Load CSV
    df = pd.read_csv('../data/movies.csv')

    # Clean column names (optional, for SQL compatibility)
    df.columns = [c.strip().replace(' ', '_') for c in df.columns]

    # Connect to SQLite (creates file if not exists)
    conn = sqlite3.connect('../db/movies.sqlite')

    # Write DataFrame to SQL table
    df.to_sql('movies', conn, if_exists='replace', index=False)

    # Read from SQL table to verify
    df = pd.read_sql_query('SELECT * FROM movies', conn)
    # print(df)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the connection is closed
    if conn:
        conn.close()
