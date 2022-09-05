#!/usr/bin/env python
import base64
import pyaes
import time
import json
import rsa

class AES_Database:
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

class RSA_Database:
    def __init__(self):
        self.database = {} # Sets the database to an empty array by default.
        self.key = None # Sets the key to none by default.
        self.public_key, self.private_key = rsa.newkeys(16) # Creates a base set of keys.

    def generate_keys(self, size=4096):
        if size < 4096:
            raise Exception('Key size too low must be above 4096!')
        self.public_key, self.private_key = rsa.newkeys(size)

    def load_keys(self, keys=None, isfile=False, filename=None):
        if isfile == False: # If it is not a file.
            keys = base64.b64decode(keys.encode()).decode().split(':-::-::-::-:') # Decodes and splits the key data.
            self.private_key = self.private_key._load_pkcs1_pem(keys[0]) # loads the private key.
            self.public_key = self.public_key._load_pkcs1_pem(keys[1]) # loads the public key.
        else:
            if filename != None: # If the filename is none.
                f = open(filename, 'rb') # Opens the file.
                keys = base64.b64decode(f.read()).decode().split(':-::-::-::-:') # Decodes and splits the key data.
                f.close() # Closes the file.
                self.private_key = self.private_key._load_pkcs1_pem(keys[0]) # loads the private key.
                self.public_key = self.public_key._load_pkcs1_pem(keys[1]) # loads the public key.
            else:
                raise Exception('Could not read database to file because filename was not specified!')

    def load_private_pem(self, pem_file):
        f = open(pem_file, 'r') # Opens the pem file.
        priv = f.read() # Reads the private key.
        f.close() # Closes the file.
        self.private_key = self.private_key._load_pkcs1_pem(priv) # Loads the private key.
    
    def load_public_pem(self, pem_file):
        f = open(pem_file, 'r') # Opens the pem file.
        pub = f.read() # Reads the public key.
        f.close() # Closes the file.
        self.public_key = self.public_key._load_pkcs1_pem(pub) # Loads the public key.

    def get_keys(self):
        return base64.b64encode(self.private_key._save_pkcs1_pem()+b':-::-::-::-:'+self.public_key._save_pkcs1_pem()).decode() # Converts the keys to an easy save format.

    def save_keys(self, filename):
        f = open(filename, 'w+') # Opens the file.
        f.write(self.get_keys()) # Writes the converted keys.
        f.close() # Closes the file.

    def create_database(self, name):
        self.database = {'name': name, 'created': str(time.ctime())} # Creates basic database.
        return self.database # Returns the database.

    def encrypt_database(self, tofile=False, filename=None):
        if self.public_key != None: # If we dont have a public key.
            encrypted = rsa.encrypt(base64.b64encode(json.dumps(self.database).encode()), self.public_key) # Encrypts the database
            if tofile == False: # Checks if the user wants the encryption to a file or returned.
                return encrypted # Returnes the encrypted json data.
            else:
                if filename != None: # If the filename is not null.
                    f = open(filename, 'wb+') # Opens the file.
                    f.write(encrypted) # Writes the encrypted data to the file.
                    f.close() # Closes the file.
                else:
                    raise Exception('Could not write database to file because filename was not specified!')
        else:
           raise Exception('You need to either generate_keys or load_keys to encrypt an rsa database.')

    def load_database(self, encrypted_db=None, isfile=False, filename=None):
        if self.private_key != None: # If we dont have a private key.
            if isfile == False: # Checks if the user wants the decryption to a file or returned.
                if encrypted_db == None:
                    raise Exception('Could not load database because encrypted_db is not specified!')
                self.database = json.loads(base64.b64decode(rsa.decrypt(encrypted_db, self.private_key))) # Decrypt the database.
                return self.database # Returnes the database.
            else:
                if filename != None: # If the filename is not null.
                    try: # Try to open the file.
                        f = open(filename, 'rb+') # Opens the file.
                        self.database = json.loads(base64.b64decode(rsa.decrypt(f.read(), self.private_key))) # Decrypt the database from loaded data.
                        f.close() # Closes the file.
                    except Exception as ex: # If the file can not be opened.
                        raise Exception('Could not open the database file!'+str(ex))
                else:
                    raise Exception('Could not read database to file because filename was not specified!')
        else:
            raise Exception('You need to either generate_keys or load_keys to load an rsa database.')
