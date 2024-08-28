CREATE TABLE IF NOT EXISTS Meshes (
           id integer PRIMARY KEY AUTOINCREMENT,
           MeshData BLOB Not Null,
           Name text NOT NULL,
           Type text CHECK( Type IN ('obj','fbx','usd') ) NOT NULL DEFAULT 'obj',
           Author text NOT NULL,
           Description text NOT NUll,
           Date text NOT NULL
);