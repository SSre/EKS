""" 8/07/2018, 05:17 PM """
# coding=utf-8
# !/usr/bin/env python

from matilda_cost.mock_data.amazon.mock_data_helper import MockDataHelper
from matilda_cost.constant.matilda_enum import FormatterConstants
from matilda_cost.cloud_providers.amazon.cost_estimation import GenericHelper
import logging as log


class JSONFormatter(object):

    def __init__(self):
        "JSON Formatter Class"
        self.mock_helper = MockDataHelper()
        self.data = self.mock_helper.get_group_by_service()

    def format_and_filter_json(self, json_to_format):
        log.info('---Format and Filter Json---')
        log.debug('The data is %s', json_to_format)
        json_to_return = dict()
        json_list = []
        if isinstance(json_to_format, list):
            for x in json_to_format:
                json_list.append(self.add_data_to_json(x))
        final_json = dict()
        final_json[FormatterConstants.response.value]= {FormatterConstants.output_metrics.value:json_list}
        final_json[FormatterConstants.response.value][FormatterConstants.unit.value] = "USD"
        final_json[FormatterConstants.response.value][FormatterConstants.title.value] = "Cost Overview"
        final_json[FormatterConstants.response.value][FormatterConstants.type.value] = "bar"
        final_json[FormatterConstants.response.value].update(
            self.create_pie_data(final_json[FormatterConstants.response.value][FormatterConstants.output_metrics.value]))
        return final_json

    def create_pie_data(self, bar_data):
        log.info('pie_data:' + str(bar_data))
        grand_total = 0
        final_data_list = list()

        main_dict = dict()
        for x in bar_data:
            inner_loop_flag = True
            grand_total += float(x['total'])
            log.debug(str(x))
            log.debug(x['total'])
            log.debug(grand_total)

            if inner_loop_flag:
                for y in x['values']:
                    if y['key'] == 'Cost':
                        log.debug('key' + y.get('key'))
                        inner_loop_flag = False
                        break

                    else:
                        if not y.get('key') in main_dict:
                            main_dict[y.get('key')] = 0
                        main_dict[y.get('key')] += float(y['value'])
                        log.debug('Key:' + str(y.get('key')))
                        log.debug('value:' + str(main_dict[y.get('key')]))

            if not inner_loop_flag:
                temp_inner_loop_dict = dict()
                temp_inner_loop_dict['category'] = x['category']
                temp_inner_loop_dict['value'] = x['total']
                final_data_list.append(temp_inner_loop_dict)

        for k, v in main_dict.items():
            temp_dict = dict()
            temp_dict['category'] = k
            temp_dict['value'] = v
            final_data_list.append(temp_dict)

        final_pie_dict = dict()
        final_pie_dict['total'] = grand_total
        final_pie_dict['pie_data'] = final_data_list

        return final_pie_dict

    def add_data_to_json(self, data_to_add):
        log.info('---Adding data to Json---')
        log.debug('The data is %s', data_to_add)
        metrics_json = {}
        metrics_json[FormatterConstants.date.value] = data_to_add[FormatterConstants.time_period.value][
            FormatterConstants.start_date.value]
        metric = self.create_metrics(data_to_add)
        metrics_json[FormatterConstants.total.value] = metric[FormatterConstants.total.value]
        metrics_json[FormatterConstants.value.value] = metric[FormatterConstants.metric.value]
        return metrics_json


    def create_metrics(self, input_json):
        log.info('---Create metrics in Progress---')
        if (GenericHelper().isNonEmptyList(input_json.get(FormatterConstants.groups.value))):
            return self.get_total_cost(self.get_value_from_json(FormatterConstants.groups.value, input_json))
        else:
            return self.get_total_cost_no_group_by(input_json.get(FormatterConstants.input_total.value))


    def get_value_from_json(self, key, json_object):
        log.info('---Get value from the Json---')
        if isinstance(json_object, dict):
            return  json_object.get(key)

    def get_total_cost(self, json_object):
        log.info('----Get Total Cost in Progress---')
        listObj = []
        total = 0
        test = ""
        if isinstance(json_object, list):
            for x in json_object:
                value_dict = {}
                test = x
                keys = x[FormatterConstants.input_keys.value]
                key = ""
                key_lenth = len(keys)
                if key_lenth == 1:
                    key = keys[0]
                elif key_lenth == 2:
                    key = str(keys[0]) + ':::' + str(keys[1])
                else:
                    raise Exception("Cannot have more than 2 keys in group by")
                value_dict[FormatterConstants.key.value] = key
                # value_dict["cost"] = x["Metrics"]["UnblendedCost"]["Amount"]
                value_dict[FormatterConstants.cost.value] = self.validate_and_retrieve_metrics(
                    x.get(FormatterConstants.input_metrics.value))
                total = total + float(value_dict[FormatterConstants.cost.value])
                listObj.append(value_dict)

        return_obj = {}
        return_obj[FormatterConstants.total.value] = total
        return_obj[FormatterConstants.metric.value] = listObj

        return return_obj

    def get_total_cost_no_group_by(self, json_object):
        log.info('---- Get Total Cost Group By in Progress---')
        log.debug('get total cost no group by: %s', str(json_object))
        listObj = []
        total = 0
        value_dict = {}

        if isinstance(json_object, dict):
            total = self.validate_and_retrieve_metrics(json_object)
        value_dict[FormatterConstants.cost.value] = total
        value_dict[FormatterConstants.key.value] = "Cost"
        listObj.append(value_dict)
        return_obj = {FormatterConstants.total.value: total, FormatterConstants.metric.value: listObj}

        return return_obj


    def validate_and_retrieve_metrics(self, metric):
        # print('metric:'+str(metric))
        # metric_dict = metric.get(FormatterConstants.input_metrics.value)
        len_metric_dict = len(metric)
        if len_metric_dict == 1:
            temp_metric_value = metric.values().__iter__().__next__()
            return temp_metric_value.get(FormatterConstants.amount.value)
        elif len_metric_dict > 1:
            raise Exception("Metrics cannot have more than one value")

