""" 8/07/2018, 05:17 PM """
# coding=utf-8
# !/usr/bin/env python

from flask import json
import os
import logging as log


class MockDataHelper(object):

    def __init__(self):
        "Mock Data Helper Class"
        self.mock_data_dir = 'amazon'
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, self.mock_data_dir))


    def use_virtual(self):
        log.info('---Using virtual data---')
        with open(self.data_dir + '/virtual.json')as f:
            data = json.load(f)
        return data["use_virtual"]

    def get_granularity(self):
        log.info('---Get Granularity in Progress---')
        try:
            with open(self.data_dir + '/granularity.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)


    def get_metrics(self):
        log.info('---Get metrics in Progress---')
        try:
            with open(self.data_dir + '/metrics.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)


    def get_filter(self):
        log.info('---Get Filter---')
        try:
            with open(self.data_dir + '/filter.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)


    def get_group_by(self):
        log.info('---Get Group By in Progress---')
        try:
            with open(self.data_dir + '/group_by.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)


    def get_group_by_service(self):
        log.info('---get Group By service in Progress---')
        try:
            with open(self.data_dir + '/group_by_service.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)


    def get_new_filter_group_by_service(self):
        log.info('---Get new filter group by service in Progress----')
        try:
            with open(self.data_dir + '/new_filter_groupby.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)

    def single_group_by_dim_cost_data(self):
        log.info('---Get single group by dim cost data in Progress---')
        try:
            with open(self.data_dir + '/single_group_by_dim_cost_data.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.strerror)

    def single_group_by_tag_cost_data(self):
        log.info('---Get single group by tag cost data in Progress---')
        try:
            with open(self.data_dir + '/single_group_by_tag_cost_data.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.strerror)

    def two_group_by_dim_cost_data(self):
        log.info('---Get Two group by dim cost data in Progress---')
        try:
            with open(self.data_dir + '/two_group_by_dim_cost_data.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.strerror)

    def two_group_by_tag_dim_cost_data(self):
        log.info('---Get Two group by Tag cost data in Progress---')
        try:
            with open(self.data_dir + '/two_group_by_tag_dim_cost_data.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.strerror)

    def no_group_by_cost_data(self):
        log.info('---Get No group by cost data in Progress---')
        try:
            with open(self.data_dir + '/no_group_by_cost_data.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.strerror)

