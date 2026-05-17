import sqlite3
import pandas as pd
import os

# 1. Connect to (or create) the database file
# This creates a file called 'pyro_planner.db' right in your project folder
conn = sqlite3.connect('pyro_planner.db')


def import_csv_to_db(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: Could not find the file at {csv_path}")
        return

    # 2. Read the CSV using pandas (the Python 'Excel' tool)
    df = pd.read_csv(csv_path)

    # 3. Save to the database (this creates the 'fireworks' table automatically)
    df.to_sql('fireworks', conn, if_exists='replace', index=False)

    print("--- SUCCESS ---")
    print(f"Imported {len(df)} fireworks into the Python database!")


# --- RUN THE IMPORT ---
# Replace this with your actual path
my_path = "C:/Users/layce/Downloads/fireworks.csv"
import_csv_to_db(my_path)

# Quick check: Print the first 5 fireworks to the console
print("\nFirst 5 Fireworks in Database:")
print(pd.read_sql('SELECT * FROM fireworks LIMIT 5', conn))


def check_firework_count():
    # Connect and count the rows
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fireworks")
    count = cursor.fetchone()[0]

    print(f"\n--- VERIFICATION ---")
    if count == 72:
        print(f"✅ Verified: All {count} fireworks are safely in the database.")
    else:
        print(f"⚠️ Warning: Database has {count} fireworks (Expected 72).")


check_firework_count()