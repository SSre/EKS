""" 8/15/2018, 10:19 AM """
# coding=utf-8
# !/usr/bin/env python

from matilda_cost.db import api as db_api


def granularity_table():
    # Insert data into the granularity table
    data = [{
            "cd": 1,
            "value": "DAILY"
        },
        {
            "cd": 2,
            "value": "MONTHLY"
        }]
    for item in data:
        db_api.create_granularity(item.get('cd'), item.get('value'))
    return True

def metrics_table():
    # Insert data into the metrics table
    data = [{
            "cd": 1,
            "value": "BlendedCost"
        },{
            "cd": 2,
            "value": "UnblendedCost"
        },{
            "cd": 3,
            "value": "UsageQuantity"
        }]
    for item in data:
        db_api.create_metrics(item.get('cd'), item.get('value'))
    return True

def config_table():
    # Insert data into the config table
    data = [{"key": 20, "Type": 2}, {"key": 20, "Type": 1}, {"key": 19, "Type": 2}, {"key": 19, "Type": 2}, {"key": 18, "Type": 2}, {"key": 18, "Type": 1},
            {"key": 17, "Type": 2}, {"key": 17, "Type": 2}, {"key": 16, "Type": 2}, {"key": 16, "Type": 1}, {"key": 14, "Type": 2}, {"key": 14, "Type": 1},
            {"key": 12, "Type": 2}, {"key": 12, "Type": 1}, {"key": 10, "Type": 2}, {"key": 9, "Type": 2}, {"key": 8, "Type": 2}, {"key": 8, "Type": 1},
            {"key": 7, "Type": 2}, {"key": 7, "Type": 1}, {"key": 6, "Type": 2}, {"key": 6, "Type": 1}, {"key": 5, "Type": 2}, {"key": 5, "Type": 1},
            {"key": 4, "Type": 2}, {"key": 4, "Type": 1}, {"key": 3, "Type": 2}, {"key": 3, "Type": 1}, {"key": 2, "Type": 2}, {"key": 2, "Type": 1},
            {"key": 1, "Type": 2}, {"key": 1, "Type": 1}]
    for item in data:
        db_api.create_config(item.get('key'), item.get('Type'))
    return True

def config_type_table():
    # Insert data into the config_type table
    data = [{
            "cd": 2,
            "value": "Filter"
        },
        {
            "cd": 1,
            "value": "GroupBy"
        }]
    for item in data:
        db_api.create_dimension(item.get('cd'), item.get('value'))
    return True

def dimension_table():
    # Insert data into the dimension table
    data = [{"cd": 1, "value": "AZ"}, {"cd": 2, "value": "INSTANCE_TYPE"}, {"cd": 3, "value": "LINKED_ACCOUNT"},
            {"cd": 4, "value": "OPERATION"}, {"cd": 5, "value": "PURCHASE_TYPE"}, {"cd": 6, "value": "REGION"},
            {"cd": 7, "value": "SERVICE"}, {"cd": 8, "value": "USAGE_TYPE"}, {"cd": 9, "value": "USAGE_TYPE_GROUP"},
            {"cd": 10, "value": "RECORD_TYPE"}, {"cd": 11, "value": "OPERATING_SYSTEM"}, {"cd": 12, "value": "TENANCY"},
            {"cd": 13, "value": "SCOPE"}, {"cd": 14, "value": "PLATFORM"}, {"cd": 15, "value": "SUBSCRIPTION_ID"},
            {"cd": 16, "value": "LEGAL_ENTITY_NAME"}, {"cd": 17, "value": "DEPLOYMENT_OPTION"}, {"cd": 18, "value": "DATABASE_ENGINE"},
            {"cd": 19, "value": "CACHE_ENGINE"}, {"cd": 20, "value": "INSTANCE_TYPE_FAMILY"}]
    for item in data:
        db_api.create_dimension(item.get('cd'), item.get('value'))
    return True

if __name__ == '__main__':
    config_type_table()
    config_table()
    granularity_table()
    dimension_table()
    metrics_table()
