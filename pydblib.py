#!/usr/bin/env python
import base64
import pyaes
import time
import json

class Database:
    def __init__(self, key):
        if type(key) == str: key = key.encode('utf8') # Encodes the key if it is a string.
        while len(key) < 32: key += b'M' # Makes sure the key is atlease 32 characters long.
        if len(key) > 32: raise Exception('Key is too long for AES. Max length: 32') # Tells the user to enter a smalelr key if the key is too long. :(
        self.key = key # Sets the key value.
        self.database = {} # Sets the database to an empty array by default.
        self.aes = pyaes.AESModeOfOperationCTR(self.key) # Initializes the AES cipher.

    def create_database(self, name):
        self.database = {'name': name, 'created': str(time.ctime())} # Creates basic database.
        return self.database # Returns the database.

    def encrypt_database(self, tofile=False, filename=None):
        encrypted = self.aes.encrypt(base64.b64encode(json.dumps(self.database).encode())) # Encrypts the database
        if tofile == False: # Checks if the user wants the encryption to a file or returned.
            return encrypted # Returnes the encrypted json data.
        else:
            if filename != None: # If the filename is not null.
                f = open(filename, 'wb+') # Opens the file.
                f.write(encrypted) # Writes the encrypted data to the file.
                f.close() # Closes the file.
            else:
                raise Exception('Could not write database to file because filename was not specified!')

    def load_database(self, encrypted_db=None, isfile=False, filename=None):
        if isfile == False: # Checks if the user wants the decryption to a file or returned.
            if encrypted_db == None:
                raise Exception('Could not load database because encrypted_db is not specified!')
            self.database = json.loads(base64.b64decode(self.aes.decrypt(encrypted_db))) # Decrypt the database.
            return self.database # Returnes the database.
        else:
            if filename != None: # If the filename is not null.
                try: # Try to open the file.
                    f = open(filename, 'rb+') # Opens the file.
                    self.database = json.loads(base64.b64decode(self.aes.decrypt(f.read()))) # Decrypt the database from loaded data.
                    f.close() # Closes the file.
                except Exception as ex: # If the file can not be opened.
                    raise Exception('Could not open the database file!'+str(ex))
            else:
                raise Exception('Could not read database to file because filename was not specified!')
