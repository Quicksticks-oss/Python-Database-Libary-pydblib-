## Python Database Libary

This libary allows the user to save and load a encrypted database file and use it.

### How to use

* First we need to import the libary by writing: `import pydblib`

* ### Setup Database
* Next we will define a key: `key = 'password123'`
* Then we make a database with this line: `db = Database(key)`
* We can make a new database by writing: `db.create_database(name='specify the name of your database here')`
* We can also set the database by writing: `db.database = json_data`

* ### Encrypt Database
* You can encrypt the database by writing: `encrypted = db.encrypt_database()`
* You can also encrypt the dabase to a file by writing: `db.encrypt_database(True, 'Specify your filename here')`

* ### Load Database
* You can load the database by writing: `db.load_database(encrypted_data_here)`
* You can also load the dabase from a file by writing: `db2.load_database(isfile=True, filename='Specify your filename here')`
