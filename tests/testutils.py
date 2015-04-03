def import_project_root():
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

def create_database(connection):
    pass


