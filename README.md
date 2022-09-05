## Python Database Library

This library allows the user to usa an encrypted database.

### How to use

* First we need to import the library by writing: `import pydblib`

### AES

* ### Setup Database
  * Next we will define a key: `key = 'password123'`
  * Then we make a database with this line: `db = AES_Database(key)`
  * We can make a new database by writing: `db.create_database(name='specify the name of your database here')`
  * We can also set the database by writing: `db.database = json_data`

* ### Encrypt Database
  * You can encrypt the database by writing: `encrypted = db.encrypt_database()`
  * You can also encrypt the dabase to a file by writing: `db.encrypt_database(True, 'Specify your filename here')`

* ### Load Database
  * You can load the database by writing: `db.load_database(encrypted_data_here)`
  * You can also load the dabase from a file by writing: `db2.load_database(isfile=True, filename='Specify your filename here')`
  
### RSA (BETA)

* ### Setup Database
  * Then we make a database with this line: `db = RSA_Database()`
  * We can make a new database by writing: `db.create_database(name='specify the name of your database here')`
  * We can also set the database by writing: `db.database = json_data`
  * We also need to make keys or load some write: `db.generate_keys()` to make new keys or `db.load_keys(key_data_here)` to load them.
  * If you have a public and private pem file you can load them with: `db.load_public_pem(filename_here)` or `db.load_private_pem(filename_here)`
  * If you need to get the keys in the save format you can use: `db.get_keys()`
  * If you want to save the keys you can write: `db.save_keys(filename_here)`

* ### Encrypt Database
  * You can encrypt the database by writing: `encrypted = db.encrypt_database()`
  * You can also encrypt the dabase to a file by writing: `db.encrypt_database(True, 'Specify your filename here')`

* ### Load Database
  * You can load the database by writing: `db.load_database(encrypted_data_here)`
  * You can also load the dabase from a file by writing: `db2.load_database(isfile=True, filename='Specify your filename here')`
