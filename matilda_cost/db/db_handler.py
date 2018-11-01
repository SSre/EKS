from matilda_cost.db import api as db_api

def get_credentials(cloud_provider, name):
    response = db_api.get_accounts(cloud_provider=cloud_provider, name=name)
    for item in response:
        account = item.get('credentials')
        return account

def get_granularity():
    response = db_api.get_granularity()
    granularity_list = []
    for item in response:
        granularity_list.append(item.get('value'))
    return granularity_list

def get_metrics():
    response = db_api.get_metrics()
    metrics_list = []
    for item in response:
        metrics_list.append(item.get('value'))
    return metrics_list

def get_group_by():
    response = db_api.get_group_by()
    groupByList = []
    for x in response:
        groupByList.append(x.value)
    return groupByList

def get_filter():
    return db_api.get_filter()

def get_request_groupby(start_dt, end_date, account_name):
    response = db_api.get_request(start_dt, end_date, account_name)
    for item in response:
        resp = item.get('groupby')
        return resp

def get_request_filterby(start_dt, end_date, account_name):
    response = db_api.get_request(start_dt, end_date, account_name)
    for item in response:
        resp = item.get('filter_by')
        return resp

def create_req(start_dt, end_date, account_name, req_data, filterby):
    data = {
        "start_dt": start_dt,
        "end_dt": end_date,
        "account_id": account_name,
        "groupby": req_data,
        "filter_by": filterby
    }
    return db_api.create_req(data)

def create_req_payload(req_data, account_name, aws, ui):
    print("hello")
    data = {
        "input_json": req_data,
        "account_id": account_name,
        "output_json_from_aws": aws,
        "output_json_for_ui": ui
    }
    return db_api.create_req_payload(data)

def get_req_payload(req_data):
    response = db_api.get_req_payload(req_data)
    print(response)
    for item in response:
        resp = item.get('output_json_for_ui')
        return resp