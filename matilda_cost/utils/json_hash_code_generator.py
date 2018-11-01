""" 8/07/2018, 05:17 PM """
# coding=utf-8
# !/usr/bin/env python

import hashlib
import canonicaljson
import logging as log
from matilda_cost.mock_data.amazon.mock_data_helper import MockDataHelper


class JSONHashGenerator(object):

    def generate_hash_for_json(self, json_to_format):
        log.info('---Format and Filter Json---')
        log.debug('The data is %s', json_to_format)
        encoded_json = canonicaljson.encode_canonical_json(json_to_format)
        return hashlib.sha3_224(encoded_json).hexdigest()


# print(JSONHashGenerator().generate_hash_for_json(MockDataHelper().single_group_by_dim_cost_data()))
# print(JSONHashGenerator().generate_hash_for_json(MockDataHelper().single_group_by_dim_cost_data()))
# print('*'*100)
# print(JSONHashGenerator().generate_hash_for_json(MockDataHelper().two_group_by_tag_dim_cost_data()))
# print('*'*100)
# print(JSONHashGenerator().generate_hash_for_json({"testa":"testb"}))
# print(JSONHashGenerator().generate_hash_for_json({"testa"          :          "testb"}))
# print(JSONHashGenerator().generate_hash_for_json({"testa"
#                                                   :
#                                                       "testb"}))