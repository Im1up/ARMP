import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('surgery_stats.db')
cursor = conn.cursor()

# Step 1: Find the SurgeryID for "Surgery E"
cursor.execute("SELECT SurgeryID FROM Surgeries WHERE SurgeryName = 'Surgery E'")
surgery_e = cursor.fetchone()

if surgery_e:
    surgery_id = surgery_e[0]
    
    # Step 2: Delete associated records in SurgeryStats and SurgeryPredictions
    cursor.execute("DELETE FROM SurgeryStats WHERE SurgeryID = ?", (surgery_id,))
    cursor.execute("DELETE FROM SurgeryPredictions WHERE SurgeryID = ?", (surgery_id,))
    
    # Step 3: Delete the surgery from the Surgeries table
    cursor.execute("DELETE FROM Surgeries WHERE SurgeryID = ?", (surgery_id,))
    
    # Commit the changes
    conn.commit()
    print("Surgery E and its associated records have been removed.")
else:
    print("Surgery E does not exist in the database.")

# Close the connection
conn.close()
