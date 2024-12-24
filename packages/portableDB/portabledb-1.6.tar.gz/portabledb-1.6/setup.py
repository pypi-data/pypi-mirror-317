from setuptools import setup, find_packages

setup(
    name='portableDB',
    version='1.6',
    author='DoubleSquad',
    description="This library is an easyest way to use local database!",
    long_description_content_type="text/markdown",
    long_description="""
    
# PortableDB Documentation

PortableDB is a lightweight, easy-to-use Python package for creating, managing, and interacting with portable databases.

## Installation

To install PortableDB, use pip:

```bash
pip install portableDB
```

## Methods

### `LogType(Type)`

Sets the logging state for the database operations.

- **Arguments:**
  - `Type` (str): Can be one of the following:
    - `'COLORFUL'`: Enables colorful logs for better readability.
    - `'BASE'`: Enables normal command-line logging.
    - `'NONE'`: Disables logging output.

### `CreateDatabase()`

Creates a new database.

- **Arguments:**
  - `name` (str): The name of the database to create (should include a file type like '.db').

### `WriteDatabase(information, cell)`

Writes data to the database.

- **Arguments:**
  - `information` (array): An array of values to write.
  - `cell` (int): The index of cell at which to write information (must be positive).

### `ReadDatabase(cell, index)`

Reads data from the database.

- **Arguments:**

  - `cell` (int): The index of cell to read.
  - `index` ('ALL' or int or just ignore):
    - `'ALL'` (string): Reads all elements in the specified cell.



- **Returns:**

  - The data read from specified cell.

### `RenameDatabase(newName)`

Renames the database.

- **Arguments:**
  - `newName` (str): The new name for the database (should not include a file type like '.db').

### `DeleteDatabase()`

Deletes the specified database.

- **Arguments:**
  - No arguments :)


    """,
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6'
    ],
)