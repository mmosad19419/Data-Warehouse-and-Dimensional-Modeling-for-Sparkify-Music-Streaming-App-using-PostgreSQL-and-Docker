from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData

def main():
    graph = create_schema_graph(metadata=MetaData('postgresql://student:student@127.0.0.1/sparkifydb'))
    graph.write_png('sparkifydb_erd.png')

if __name__ == "__main__":
    main()