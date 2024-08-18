import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('surgery_stats.db')
cursor = conn.cursor()

# Update surgery names
cursor.execute("UPDATE Surgeries SET SurgeryName = 'Firs' WHERE SurgeryID = 1")
cursor.execute("UPDATE Surgeries SET SurgeryName = 'FRMC' WHERE SurgeryID = 2")
cursor.execute("UPDATE Surgeries SET SurgeryName = 'Beam Park' WHERE SurgeryID = 3")
cursor.execute("UPDATE Surgeries SET SurgeryName = 'Forest' WHERE SurgeryID = 4")

# Create a table for predictions if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS SurgeryPredictions (
    PredictionID INTEGER PRIMARY KEY AUTOINCREMENT,
    SurgeryID INTEGER,
    Date DATE DEFAULT CURRENT_DATE,
    PredictedTasks INTEGER DEFAULT 0,
    PredictedRegistrations INTEGER DEFAULT 0,
    PredictedDocuments INTEGER DEFAULT 0,
    PredictedReferrals INTEGER DEFAULT 0,
    FOREIGN KEY (SurgeryID) REFERENCES Surgeries(SurgeryID)
)
''')

conn.commit()
conn.close()
