#based on Jon Macey's code

import sqlite3
from sqlite3 import Error

"""generate a new Meshes db file and generate the tables

    Parameters
    ----------
    file : str
        the file to generate for the databse, a full path can be passed as well as the name.        

        Returns
        -------
            bool
                True if database file can be created.
"""


def create_new_database(path: str) -> bool:
    try:
        with sqlite3.connect(path) as connection:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS Meshes (
                id integer PRIMARY KEY AUTOINCREMENT,
                Name text NOT NULL,
                Author text NOT NULL,
                Description text NOT NULL,
                Date text NOT NULL,
                MeshData BLOB NOT NULL,
                FileType TEXT CHECK( FileType IN ('obj','usd','fbx') )   NOT NULL DEFAULT 'obj'
                );
            """

            cursor = connection.cursor()
            cursor.execute(create_table_sql)
            return True
    except Error as e:
        print(e)
        return False