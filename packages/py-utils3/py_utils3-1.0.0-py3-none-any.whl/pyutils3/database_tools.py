# smart_library/database_tools.py
import pickle
import os

def save(data, db_file=database_file):
    """Save data to a database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
    else:
        db = {}

    db.update(data)

    with open(db_file, 'wb') as file:
        pickle.dump(db, file)
    return "Data saved."

def load(db_file=database_file):
    """Load data from a database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
        return db
    else:
        return "No data found."
