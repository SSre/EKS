""" 8/08/2018, 03:51 PM """
# coding=utf-8
# !/usr/bin/env python

from matilda_cost.db import db_handler
from matilda_cost.cloud_providers.amazon.cost_estimation import AWSCostEstimate
from matilda_cost.mock_data.amazon.mock_data_helper import MockDataHelper
from matilda_cost.utils.json_formatter import JSONFormatter
import logging as log

def get_granularity():
    helper = MockDataHelper()
    if helper.use_virtual():
        return helper.get_granularity()
    return db_handler.get_granularity()

def get_metrics():
    helper = MockDataHelper()
    if helper.use_virtual():
        return helper.get_metrics()
    return db_handler.get_metrics()

def get_groupby(start_date, end_date, account_name):
    helper = MockDataHelper()
    if helper.use_virtual():
        return helper.get_group_by()
    groupByList = db_handler.get_group_by()
    generic_values_service = AWSCostEstimate(account_name=account_name)
    groupByDict = dict()
    groupByDict["Tag"] = generic_values_service.get_tags(start_date, end_date)["Tags"]
    groupByDict['Dimension'] = groupByList
    return groupByDict

def get_filterby(start_date, end_date, account_name):
    helper = MockDataHelper()
    if helper.use_virtual():
        return helper.get_filter()
    response = db_handler.get_filter()
    generic_values_service = AWSCostEstimate(account_name=account_name)
    filterDimensionDict = dict()
    for item in response:
        filter_by_dimensions = generic_values_service.get_dimension_values(item.value, start_date, end_date)
        filter_by_dimension_temp_list = []
        for y in filter_by_dimensions["DimensionValues"]:
            filter_by_dimension_temp_list.append(y["Value"])
        filterDimensionDict[item.value] = filter_by_dimension_temp_list

    filter_tag_base = generic_values_service.get_tags(start_date, end_date)

    filterTagsDict = dict()
    for a in filter_tag_base["Tags"]:
        filterTagsDict[a] = generic_values_service.get_tag_values(a, start_date, end_date)["Tags"]

    filterDict = dict()
    filterList = list()
    print(filterDimensionDict)
    for key, value in filterDimensionDict.items():
        filter_by_dict = dict()
        filter_by_dict['Title'] = key
        filter_by_dict['Values'] = value
        filterList.append(filter_by_dict)
    filterDict['Dimension'] = filterList
    filterDict['Tag'] = filterTagsDict
    return filterDict

def cost_estimation(req_data, account_name):
    json_formatter = JSONFormatter()
    generic_service = AWSCostEstimate(account_name=account_name)
    db_check = db_handler.get_req_payload(req_data)
    if db_check is not None:
        return db_check
    response = generic_service.generic_service(req_data)
    resp = json_formatter.format_and_filter_json(response)
    db_handler.create_req_payload(req_data, account_name, response, resp)
    return resp

def get_group_by(start_date, end_date, account_name):
    db_check = db_handler.get_request_groupby(start_date, end_date, account_name)
    if db_check is not None:
        return db_check
    group_by = get_groupby(start_date, end_date, account_name)
    filter_by = get_filterby(start_date, end_date, account_name)
    db_handler.create_req(start_date, end_date, account_name, group_by, filter_by)
    return group_by

def get_filter(start_date, end_date, account_name):
    db_check = db_handler.get_request_filterby(start_date, end_date, account_name)
    if db_check is not None:
        return db_check
    group_by = get_groupby(start_date, end_date, account_name)
    filter_by = get_filterby(start_date, end_date, account_name)
    db_handler.create_req(start_date, end_date, account_name, group_by, filter_by)
    return filter_by
