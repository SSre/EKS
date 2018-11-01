""" 8/07/2018, 04:24 PM """
# coding=utf-8
# !/usr/bin/env python

import datetime
import str2bool
from matilda_cost.constant.matilda_enum import GroupByConstants, FilterByConstants
import logging as log


class GenericHelper(object):

    def __init__(self):
        "Generic Helper Class"

    def validate_and_return_single_valued_list(self, list_to_check, list_name):
        if isinstance(list_to_check, list):
            if len(list_to_check) == 1:
                return list_to_check[0]
            else:
                raise Exception("Not a single valued List:" + list_name)


    def dictionary_key_exist(self, key, dict_object):
        if isinstance(dict_object, dict):
            if key in dict_object:
                return True
            else:
                return False

    def isNonEmptyDict(self, dict_object):
        is_non_empty_dict = False;
        if isinstance(dict_object, dict) and len(dict_object.keys())>0:
            is_non_empty_dict = True
        return  is_non_empty_dict

    def isNonEmptyList(self, list_object):
        is_non_empty_list = False
        if isinstance(list_object, list) and len(list_object)>0:
            is_non_empty_list = True
        return  is_non_empty_list

    def validate_date_format(self, date_text):
        #print(date_text)
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

class GroupByHelper(GenericHelper):

    def __init__(self):
        "Group By helper Class"
        GenericHelper.__init__(self)

    # This method is for creating individual components for group by
    def create_component(self, group_by_type=GroupByConstants.default_group_by_type.value, key=GroupByConstants.default_group_by_key.value):
        log.info('---Create component---')
        component = {"Type": group_by_type, "Key": key}
        log.debug('The Component is %s', component)
        return component


    # This method takes list of keys and convert it into list of components
    def create_group_by_components(self, group_by_type=GroupByConstants.default_group_by_type.value, keys=[]):
        log.info('---Create group by component---')
        log.debug('Keys Type %s', type(keys))
        group_by_component_list = []
        if len(keys) == 0 or not isinstance(keys, list):
            raise Exception("Key List(Dimensions/Tags) should be a non empty list")
        else:
            for x in keys:
                group_by_component_list.append(self.create_component(group_by_type=group_by_type, key=x))
        return group_by_component_list


    # Helper for Tags to pass keys and get tag components
    def create_group_by_tags(self, keys=[]):
        if len(keys) != 0 and isinstance(keys, list):
            return self.create_group_by_components(group_by_type=GroupByConstants.group_by_tag.value, keys=keys)
        else:
            raise Exception("Tag Keys should be a non empty list")


    # Helper for Dimensions to pass keys and get tag components
    def create_group_by_dimensions(self, keys=[]):
        if len(keys) != 0 and isinstance(keys, list):
            return self.create_group_by_components(group_by_type=GroupByConstants.group_by_dimension.value, keys=keys)
        else:
            raise Exception("Tag Keys should be a non empty list")


    # this method takes list of dimensions and tags and consolidate into a single group by
    def create_group_by(self, tags=[], dimensions=[]):
        group_by = []
        size_of_tags = len(tags)
        size_of_dimensions = len(dimensions)
        size_of_group_by = size_of_tags + size_of_dimensions
        # This is current restriction at main end to limit max of 2 group by
        if size_of_group_by > GroupByConstants.max_group_by.value:
            raise Exception("Currently Matilda Supports only two Group By")
        elif size_of_group_by == 0:
            return group_by
        else:
            if size_of_tags > 0 and isinstance(tags, list):
                print(self.create_group_by_tags(tags))
                group_by.extend(self.create_group_by_tags(tags))
            if size_of_dimensions > 0 and isinstance(dimensions, list):
                print(self.create_group_by_dimensions(dimensions))
                group_by.extend(self.create_group_by_dimensions(dimensions))
        log.debug('Group By %s', group_by)
        return group_by

    def create_group_by_new(self, content):
        group_by = []
        group_by_dict = content.get("GroupBy")
        log.debug('group by dict %s', group_by_dict)
        if not GenericHelper.isNonEmptyDict(self, group_by_dict):
            return group_by
        dimension_list = group_by_dict.get("Dimensions")
        tag_list = group_by_dict.get("Tags")
        dimension_list_size = 0
        tag_list_size = 0

        if not (dimension_list is None):
            dimension_list_size = len(dimension_list)

        if not (tag_list is None):
            tag_list_size = len(tag_list)
        total_size_of_group_by = dimension_list_size + tag_list_size

        if total_size_of_group_by > 2:
            raise Exception("Currently Matilda Supports only two Group By")

        elif total_size_of_group_by == 0:
            return group_by

        elif total_size_of_group_by == 1:
            if dimension_list_size == 1:
                dimension_keys = []
                dimension_keys.append(dimension_list[0].get("Key"))
                group_by.extend(self.create_group_by_dimensions(dimension_keys))
            elif tag_list_size == 1:
                tag_keys = []
                tag_keys.append(tag_list[0].get("Key"))
                group_by.extend(self.create_group_by_tags(tag_keys))

        elif total_size_of_group_by == 2:
            if dimension_list_size == 2:
                dimension_keys = []
                second_dimension = ""
                first_dimension = ""
                order_count = 0
                for x in dimension_list:
                    if int(x.get("Order")) == 1 and not order_count > 0:
                        order_count += 1
                        first_dimension = x.get("Key")
                    else:
                        second_dimension = x.get("Key")

                dimension_keys.append(first_dimension)
                dimension_keys.append(second_dimension)
                group_by.extend(self.create_group_by_dimensions(dimension_keys))

            elif tag_list_size == 2:
                tag_keys = []
                first_tag = ""
                second_tag = ""
                for x in tag_list:
                    if int(x.get("Order")) == 1:
                        first_tag = x.get("Key")
                    else:
                        second_tag = x.get("Key")

                tag_keys.append(first_tag)
                tag_keys.append(second_tag)
                group_by.extend(self.create_group_by_tags(tag_keys))


            elif dimension_list_size == 1 and tag_list_size == 1:
                tag_keys = []
                dim_keys = []
                order_1 = ""

                log.debug("is dimension order equal to 1:" + str(int((dimension_list[0].get("Order")) == 1)))

                if int(dimension_list[0].get("Order")) == 1:
                    order_1 = "dim"

                tag_keys.append(tag_list[0].get("Key"))
                dim_keys.append(dimension_list[0].get("Key"))

                if order_1 == "dim":
                    group_by.extend(self.create_group_by_dimensions(dim_keys))
                    group_by.extend(self.create_group_by_tags(tag_keys))

                else:
                    group_by.extend(self.create_group_by_tags(tag_keys))
                    group_by.extend(self.create_group_by_dimensions(dim_keys))

        return group_by

class FilterHelper(GenericHelper):

    def __init__(self):
        GenericHelper.__init__(self)

    def parse_filter_component_from_api(self, filter):
        log.info('---Filter Component from API---')
        if GenericHelper.isNonEmptyDict(self, filter):
            dimensions = filter.get("Dimensions")
            tags = filter.get("Tags")
        return  {"Dimensions": dimensions, "Tags":tags}

    def process_Dimensions(self, filter_components):
        log.info('----Process Dimensions in Progress---')
        dimensions = filter_components.get("Dimensions")
        tags = filter_components.get("Tags")
        filter_list = []

        if GenericHelper.isNonEmptyList(self, dimensions):
            for x in dimensions:
                dim_Key = x["Key"]
                dim_values = x["Values"]
                Exclude = x["Exclude"]
                dim_dict = {"Dimensions": {"Key":dim_Key, "Values":dim_values}, "Exclude":Exclude}
                filter_list.append(dim_dict)
                log.debug('Dimensions Dictionary %s', dim_dict)

        if GenericHelper.isNonEmptyList(self, tags):
            for x in tags:
                tag_Key = x.get("Key")
                tag_values = x.get("Values")
                Exclude = x["Exclude"]
                tag_dict = {"Tags": {"Key":tag_Key, "Values":tag_values}, "Exclude":Exclude}
                log.debug('Tag Dictionary %s', tag_dict)
                filter_list.append(tag_dict)

        log.debug('The Filter List %s', filter_list)
        return  filter_list


    def sort_filter_components(self, filter_list):
        include_list = []
        not_list = []
        for x in filter_list:

            if str2bool.str2bool(x.get("Exclude")):
                x.pop("Exclude")
                not_list.append(x)
            else:
                x.pop("Exclude")
                include_list.append(x)

        for x in not_list:
            include_list.append({"Not":x})

        if(len(include_list)>1):
            filter_final =  {"And":include_list}
        elif (len(include_list) == 1):
            filter_final = include_list[0]
        log.debug('The final filter list is %s', filter_final)
        return filter_final

    def create_filter(self, content):
        log.debug("content to filter: %s", str(content))
        final_filter_component = self.sort_filter_components(self.process_Dimensions(self.parse_filter_component_from_api(content)))
        log.debug('final filter component is %s', final_filter_component)
        return final_filter_component
