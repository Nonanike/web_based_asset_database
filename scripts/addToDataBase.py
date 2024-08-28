import argparse

from Core import Connection

def add_mesh(
        database : str,
        meshData : str,
        name : str,
        type : str,
        author: str,
        description: str,
        date: str,
    ):

    print("add to db")
    with Connection.MeshesConnection(database) as connection :
        connection.add_item(meshData,name,type,author,description,date)

if __name__ == "__main__" :
    parser=argparse.ArgumentParser(description="Add mesh to Meshes database")
    parser.add_argument("--database","-db",help="Which Database to add to", required=True)
    parser.add_argument("--meshData","-m",help="Mesh file to add", required=True)
    parser.add_argument("--name","-n",help="Name to add", required=True)
    parser.add_argument("--type","-t",help="mesh type loaded", required=True)
    parser.add_argument("--author","-a", help="Author of query", required=True)
    parser.add_argument("--description", "-d", help="Description", required=True)
    parser.add_argument("--date", "-da", help="Date of the mesh", required=True)

    args=parser.parse_args()

    add_mesh(
        args.database,
        args.name,
        args.type,
        args.author,
        args.description,
        args.date,
        args.mesh,
    )