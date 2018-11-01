""" 8/07/2018, 04:24 PM """
# coding=utf-8
# !/usr/bin/env python

import datetime
import boto3, botocore
from botocore.exceptions import ClientError, ParamValidationError
import logging as log
from matilda_cost.cloud_providers.amazon.cost_estimation_helper import GenericHelper, FilterHelper, GroupByHelper
from matilda_cost.constant.matilda_enum import Field
from matilda_cost.db import db_handler


class AWSCostEstimate(object):
    def __init__(self, account_name):
        self.credentials = db_handler.get_credentials(cloud_provider='aws', name=account_name)
        self.conn = boto3.client('ce', region_name=self.credentials.get('region_name'),
                                 aws_access_key_id=self.credentials.get('aws_access_key_id'),
                                 aws_secret_access_key=self.credentials.get('aws_secret_access_key'))

    def generic_service(self, content):
        # Creating a generic service which accepts json and modify the data accordingly. If an empty json is passed,
        # it will return cost for past 30 days with granularity daily and un blended cost
        results = []
        token = None
        filter_from_content = self.get_filter(content)
        log.debug('Filter from content is %s', filter_from_content)
        while True:
            if token:
                kwargs = {'NextPageToken': token}
            else:
                kwargs = {}

            log.info('Get Time Period is %s', self.get_time_period(content))
            log.info('Get Granularity %s', self.get_granularity(content))
            log.info('Get metrics %s', self.get_metrics(content))
            log.info('Group by Content %s', self.get_group_by(content))
            log.info('Filter by Content %s', self.get_filter(content))

            # this condition is a workaround: AWS cost explorer does not accept empty filters currently
            if len(filter_from_content) == 0:
                try:
                    data = self.conn.get_cost_and_usage(
                        TimePeriod=self.get_time_period(content),
                        Granularity=self.get_granularity(content),
                        Metrics=self.get_metrics(content),
                        GroupBy=self.get_group_by(content),
                        **kwargs
                    )
                    log.debug('The data is %s', data)
                except (ClientError, ParamValidationError) as ce:
                    log.error('the error message is %s', ce.message)
                    return str(ce.message)
            else:
                try:
                    data = self.conn.get_cost_and_usage(
                        TimePeriod=self.get_time_period(content),
                        Granularity=self.get_granularity(content),
                        Metrics=self.get_metrics(content),
                        Filter=filter_from_content,
                        GroupBy=self.get_group_by(content),
                        **kwargs
                    )
                    log.debug('The data is %s', data)
                except (ClientError, ParamValidationError) as ce:
                    log.error('the error message is %s', ce.message)
                    return str(ce.message)

            results += data['ResultsByTime']
            token = data.get('NextPageToken')
            if not token:
                break

        return results


    def get_time_period(self, content):
        log.info('----Get Time Period---')
        time_period = ""
        Helper = GenericHelper()
        if Helper.dictionary_key_exist(Field.time_period.value, content):
            time_period = content[Field.time_period.value]
        else:
            # initializing time_period to past 30 days in case its not available in json. It is a mandatory field
            now = datetime.datetime.utcnow()
            time_period = {
                "Start": (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
                "End": now.strftime('%Y-%m-%d')
            }
        return time_period


    def get_granularity(self, content):
        log.info('---Get Granularity---')
        # defaulting granularity to daily in case it is not passed in json. It is a mandatory field
        granularity = "DAILY"
        Helper = GenericHelper()
        if Helper.dictionary_key_exist(Field.granularity.value, content):
            granularity = Helper.validate_and_return_single_valued_list(content[Field.granularity.value],
                                                                        Field.granularity.value)
        return granularity


    def get_metrics(self, content):
        log.info('---Get Metrics---')
        # initializing metrics to UnblendedCost if its not available in json. It is a mandatory field
        metrics = ["UnblendedCost"]
        Helper = GenericHelper()
        if (Helper.dictionary_key_exist(Field.metrics.value, content)):
            metrics = content[Field.metrics.value]

        return metrics


    def get_group_by(self, content):
        log.info('---Get Group By in Progress---')
        group_by = []
        Helper = GroupByHelper()
        group_by = Helper.create_group_by_new(content)
        return group_by


    def get_filter(self, content):
        log.info('---Get Filter By in Progress---')
        filter_component = {}
        Helper = GenericHelper()
        Filter = FilterHelper()
        if Helper.dictionary_key_exist(Field.filter.value, content):
            filter_component = Filter.create_filter(content.get(Field.filter.value))
        return filter_component

    def get_dimension_values(self, dimension, start_date, end_date):
        log.info('---Get Dimension Values in Progress---')
        Helper = GroupByHelper()
        Helper.validate_date_format(start_date)
        Helper.validate_date_format(end_date)
        try:
            response = self.conn.get_dimension_values(
                TimePeriod={'Start': start_date, 'End': end_date},
                Dimension=dimension
            )
            log.debug('The response is %s', response)
            return response
        except (ClientError, ParamValidationError) as ce:
            log.error('the error message is %s', ce.message)
            return str(ce.message)


    def get_tags(self, start_date, end_date):
        log.info('---Get Tags in Progress---')
        Helper = GroupByHelper()
        Helper.validate_date_format(start_date)
        Helper.validate_date_format(end_date)
        try:
            response = self.conn.get_tags(
                TimePeriod={'Start': start_date, 'End': end_date}
            )
            log.debug('The response is %s', response)
            return response
        except (ClientError, ParamValidationError) as ce:
            log.error('the error message is %s', ce.message)
            return str(ce.message)


    def get_tag_values(self, tag, start_date, end_date):
        log.info('---Get Tag values in Progress---')
        Helper = GroupByHelper()
        Helper.validate_date_format(start_date)
        Helper.validate_date_format(end_date)
        try:
            response = self.conn.get_tags(
                TimePeriod={'Start': start_date, 'End': end_date},
                TagKey=tag
            )
            log.debug('The response is %s', response)
            return response
        except (ClientError, ParamValidationError) as ce:
            log.error('the error message is %s', ce.message)
            return str(ce.message)