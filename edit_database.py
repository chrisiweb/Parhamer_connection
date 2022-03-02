from tinydb import TinyDB, Query
from config_start import path_programm
import os


path_database = os.path.join(path_programm, "_database", "_database.json")
_database = TinyDB(path_database)

# table_lama = _database.table('table_lama_1')
# table_lama = _database.table('table_lama_2')
# table_lama = _database.table('table_cria')
tables = ['table_lama_1', 'table_lama_2', 'table_cria']

for table_lama in tables:
    _database.table(table_lama).update({'gruppe': False})

print('done')
