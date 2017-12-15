'''
Created on December 7th

@author: gbaufake

Model for Alert Information
'''
import uuid


class Alert:
    def __init__(self, category):
        self.category = category
        self.description = "Alert-" + str(uuid.uuid4())

    def key(self):
        return self.category.name


    def category_value(self):
        return self.category.value[0]

    def category_description(self):
        return self.category.value[1]

    def operator(self):
        if not (self.key() == 'jvm_heap_used' or self.key() == 'jvm_non_heap_used'):
            return '>='
        else:
            return None


    def fields_for_ui(self):
        key= {
            'jvm_accumulated_gc_duration': ['value_mw_garbage_collector'],
            'jvm_heap_used': ['value_mw_greater_than', 'value_mw_less_than'],
            'jvm_non_heap_used': ['value_mw_greater_than', 'value_mw_less_than']
        }.get(self.key(), ['value_mw_threshold'])

        values = {
            'jvm_heap_used': ['20', '10'],
            'jvm_non_heap_used': ['20', '10']
        }.get(self.key(), [0])


        return zip(key, values)