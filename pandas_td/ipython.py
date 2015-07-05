# ipython.py

import re
import sys
import pandas as pd
import pandas_td as td
import tdclient

MAGIC_CONTEXT_NAME = '_td_magic_context'

class MagicContext(object):
    def __init__(self, database):
        self.database = database

    def connect(self):
        return td.connect()

def get_magic_context():
    return get_ipython().ev(MAGIC_CONTEXT_NAME)

def magic_use(line):
    ctx = MagicContext(line)
    try:
        tables = ctx.connect().client.tables(ctx.database)
    except tdclient.api.NotFoundError:
        sys.stderr.write("ERROR: Database '{0}' not found.".format(ctx.database))
        return
    # variables
    variables = {}
    variables[MAGIC_CONTEXT_NAME] = ctx
    for tbl in tables:
        d = pd.DataFrame(tbl.schema, columns=['field', 'type'])
        d.object = tbl
        variables[tbl.name] = d
    get_ipython().push(variables)
    # return value
    columns = ['name', 'count', 'estimated_storage_size', 'last_log_timestamp', 'created_at']
    return pd.DataFrame([[getattr(tbl, c) for c in columns] for tbl in tables], columns=columns)

def magic_databases(pattern):
    ctx = get_magic_context()
    databases = [db for db in ctx.connect().client.databases() if re.search(pattern, db.name)]
    columns = ['name', 'count', 'permission', 'created_at', 'updated_at']
    return pd.DataFrame([[getattr(db, c) for c in columns] for db in databases], columns=columns)

def magic_tables(pattern):
    ctx = get_magic_context()
    tables = [t for t in ctx.connect().client.tables(ctx.database) if re.search(pattern, t.identifier)]
    columns = ['name', 'count', 'estimated_storage_size', 'last_log_timestamp', 'created_at']
    return pd.DataFrame([[getattr(tbl, c) for c in columns] for tbl in tables], columns=columns)

def magic_query_with_type(line, cell, engine_type, **kwargs):
    ctx = get_magic_context()
    if line:
        database = line
    else:
        database = ctx.database
    engine = td.create_engine('{0}:{1}'.format(engine_type, database), con=ctx.connect())
    return td.read_td_query(cell, engine, **kwargs)

# extension

def load_ipython_extension(ipython):
    # %use database
    ipython.register_magic_function(magic_use, magic_kind='line', magic_name='use')

    # %dbs [PATTERN]
    ipython.register_magic_function(magic_databases, magic_kind='line', magic_name='dbs')

    # %tables [PATTERN]
    ipython.register_magic_function(magic_tables, magic_kind='line', magic_name='tables')

    # %%hive, %%pig, %%presto
    # %%hive_ts, %%pig_ts, %%presto_ts
    for name in ['hive', 'pig', 'presto']:
        def magic_query(line, cell):
            return magic_query_with_type(line, cell, name)
        def magic_query_ts(line, cell):
            return magic_query_with_type(line, cell, name, index_col='time', parse_dates={'time': 's'})
        ipython.register_magic_function(magic_query, magic_kind='cell', magic_name=name)
        ipython.register_magic_function(magic_query_ts, magic_kind='cell', magic_name=name + '_ts')
