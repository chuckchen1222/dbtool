import os

SQLFILEDIR = '/root/dbtool/dmlsql/sqlfiles/'
def handle_uploaded_file(new_filename, f):
    if not os.path.exists(SQLFILEDIR):
        os.makedirs(SQLFILEDIR)
    with open(os.path.join(SQLFILEDIR, new_filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def readFile(filename):
    file = open(os.path.join(SQLFILEDIR,filename),'r')
    sql = file.readlines()
    return sql