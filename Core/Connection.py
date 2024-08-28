#based on Jon Macey's code

import sqlite3
from sqlite3 import Error

"""class to make a connection to a Meshes and execute commands, it allows the use of Context managers
"""
con = sqlite3.connect("Meshes.db")
cur = con.cursor()

class MeshesConnection:
    """
    Parameters :
        name : str the name of the database to connect to
    """

    def __init__(self, name: str):
        self.name = name
        self.connection = None

    def open(self):
        try:
            self.connection = sqlite3.connect(self.name)
        except Error as e:
            print(f"error {e} with database {self.name}")

    def close(self):
        self.connection.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def _loadBlob(self, filename: str):
        with open(filename, "rb") as file:
            blobData = file.read()
        return blobData

    def add_item(
        self,
        meshData: str,
        name: str,
        type: str,
        author: str,
        description: str,
        date: str,
    ):
        Type = "obj"
        if meshData.endswith(".fbx"):
            Type = "fbx"
        elif meshData.endswith(".usd"):
            Type = "usd"

        cursor = self.connection.cursor()
        query = """ INSERT INTO Meshes
                                  (MeshData, Name, Type, Author, Description, Date) 
                                  VALUES (?,?,?,?,?,?)"""
        mesh_blob = self._loadBlob(meshData)

        query_data = (
            mesh_blob,
            name,
            type,
            author,
            description,
            date,
        )
        cursor.execute(query, query_data)
        self.connection.commit()
        cursor.close()

    def extract_mesh(self, name: str, out_name: str):
        cursor = self.connection.cursor()
        query = """SELECT MeshData,Type FROM Meshes WHERE Name = ?;"""
        cursor.execute(query, [name])
        record = cursor.fetchone()
        if record is not None:
            if not out_name.endswith(record[1]):
                out_name = f"{out_name}.{record[1]}"
            with open(out_name, "wb") as file:
                file.write(record[0])

        cursor.close()