#!/usr/bin/env python
from pydblib import * # imports the libary

if __name__ == '__main__':
    print('Encrypting database.')

    db = Database(key='password123') # Creates the database.
    db.create_database(name='Example database') # Creates the database.
    encrypted = db.encrypt_database() # Encrypt the database.

    print('Database:', db.database)
    print('Encrypted database:', encrypted)
    
    print()
    print('Loading and decrypting database.')

    db2 = Database(key='password123') # Makes the second database.
    db2.load_database(encrypted) # Loads the encrypted database.

    print('Loaded database:',db2.database)
