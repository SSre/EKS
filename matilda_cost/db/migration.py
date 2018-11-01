from matilda_cost.db.sqlalchemy import migration as IMPL


def db_sync(version=None, database='matilda_cost'):
    return IMPL.db_sync(version=version, database=database)


def db_version(database='matilda_cost'):
    return IMPL.db_version(database=database)


def db_initial_version(database='matilda_cost'):
    return IMPL.db_initial_version(database=database)