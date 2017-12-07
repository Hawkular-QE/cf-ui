from alert import Alert
from alert_category import AlertCategory


class AlertFactory:
    def fields_for_ui(self, category, values):
        key= {
            'jvm_accumulated_gc_duration': ['value_mw_garbage_collector'],
            'jvm_heap_used': ['value_mw_greater_than', 'value_mw_less_than'],
            'jvm_non_heap_used': ['value_mw_greater_than', 'value_mw_less_than']
        }.get(category, ['value_mw_threshold'])

        return zip(key, values)


    # Factory Method
    def create_alert(self, description, category, values):
        alertCategory = AlertCategory[category]
        alert = Alert()
        alert.description = description
        alert.category = alertCategory.value
        alert.fields = self.fields_for_ui(alertCategory.name, values)

        return alert




