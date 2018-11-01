from matilda_cost.db.sqlalchemy import api as IMPL

def get_accounts(cloud_provider, name):
    return IMPL.get_accounts(cloud_provider, name)

def get_granularity():
    return IMPL.get_granularity()

def get_metrics():
    return IMPL.get_metrics()

def get_group_by():
    return IMPL.get_group_by()

def get_filter():
    return IMPL.get_filter()

def create_dimension(id, value):
    return IMPL.create_dimension(id, value).to_dict()

def create_account(name, cloud_provider, credentials):
    return IMPL.create_account(name, cloud_provider, credentials).to_dict()

def create_config_type(id, value):
    return IMPL.create_config_type(id, value).to_dict()

def create_config(key, type):
    return IMPL.create_config(key, type).to_dict()

def create_granularity(id, value):
    return IMPL.create_granularity(id, value).to_dict()

def create_metrics(id, value):
    return IMPL.create_metrics(id, value).to_dict()

def update_account(account_id, name, credentials):
    return IMPL.update_account(account_id, name, credentials)

def create_req(data):
    return IMPL.create_req(data)

def create_req_payload(data):
    return IMPL.create_req_payload(data)

def get_request(start_dt, end_dt, account_name):
    return IMPL.get_req(start_dt, end_dt, account_name)

def get_req_payload(input_json):
    return IMPL.get_req_payload(input_json)