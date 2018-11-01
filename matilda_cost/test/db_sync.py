#run this file in order to create tables along with schema mentioned
from matilda_cost.db import migration

migration.db_sync(database='matilda_cost')
