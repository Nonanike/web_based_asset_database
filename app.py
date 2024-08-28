import sqlite3

import io
import os
# from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from Core.Connection import MeshesConnection

import json

"""
    This is a Flask app that handles uploading, viewing and downloading 3D mesh 
    online through html forms and saves the info to the database Meshes.db and 
    the uploaded files to folder 'mesh'
"""

app=Flask(__name__)

#Defining the upload folder
UPLOAD_FOLDER = './mesh'
ALLOWED_EXTENSIONS = {'obj','fbx','usd'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#Creating and checking the tables
with MeshesConnection('Meshes.db') as db:
    cursor = db.connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Meshes(id integer PRIMARY KEY AUTOINCREMENT, MeshData BLOB Not Null, Name text NOT NULL, Type text NOT NULL, Author text NOT NULL, Description text NOT NUll, Date text NOT NULL)")
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"{tables}")

@app.route ('/')

def index():
    return render_template('index.html')

#Adding the form info and files
@app.route ('/addMesh.html', methods=['GET','POST'])

def addMesh():

    """
    Handles the upload of a mesh file and form into 
    into the database and the path file.
    
    Return: Redirects url back to the main page (index.html) when successful.
    """
    
    if request.method == "POST":
        meshData = request.files['meshData']
        name = request.form.get("name")
        type = request.form.get("type")
        author = request.form.get("author")
        description = request.form.get("description")
        date = request.form.get("date")

        #Saving files to a location
        mesh_path = os.path.join(app.config['UPLOAD_FOLDER'], meshData.filename )
        meshData.save(mesh_path)

        #Adding meshes to the database
        with MeshesConnection('Meshes.db') as connection:
            connection.add_item(mesh_path,name,type,author,description,date)

        return redirect(url_for('index'))

    return render_template('addMesh.html')

#Viewing contents of the Meshes.db
@app.route('/viewDatabase.html')
def viewDatabase():
    """
    Handles viewing the contests of the Meshes.db.
    
    Return: Returns template for viewDatabase.html.
    """
    
    with MeshesConnection('Meshes.db') as connection:
        cursor = connection.connection.cursor()
        cursor.execute("SELECT id,name,type,author,description,date FROM Meshes;")
        tables = cursor.fetchall()

        for row in tables:
            id = row[0]
            name = row[1]
            type = row[2]
            author = row[3]
            description = row[4]
            date = row[5]

    return render_template('viewDatabase.html',tables=tables)

#Downloading 3D mesh files
@app.route('/viewDatabase/<int:mesh_id>',methods=['GET'])

def download(mesh_id: str):

    """
    Handles the download of a mesh file.
    
    Parameters :
    mesh id: str -- The id of the file to download.

    Return: Requested file as an attachement.
    """
    
    #Connecting to the database and retriving mesh_id to locate the requested file
    print(f"Download mesh with id: {mesh_id}")
    if request.method == 'GET':
        with MeshesConnection('Meshes.db') as connection:
            cursor = connection.connection.cursor()
            upload = cursor.execute("SELECT id, Name, Type FROM Meshes WHERE id = ?", str(mesh_id)).fetchone()
       
            if not upload:
                return "File not found", 404

            filename = f"{upload[1]}.{upload[2]}"

            mesh_directory = os.path.join(app.root_path, 'mesh')
            print(f"mesh_directory = {mesh_directory} ")

            connection.close()

            fullpath = os.path.join(mesh_directory, filename)

            print(f"{fullpath}")

            print(f"{upload[1]}.{upload[2]}")

            if not os.path.isfile(fullpath):
                return "File not found", 404

            #Returning the requested file    
            return send_from_directory(mesh_directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
