import uuid

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
        alert.category_key = alertCategory.name
        alert.fields = self.fields_for_ui(alertCategory.name, values)

        return alert


    def all_alerts(self):
        alerts = []
        for category in AlertCategory:
            alert = Alert()

            if category.name == 'jvm_heap_used' or category.name == 'jvm_non_heap_used':
                values = [20, 10]
            else:
                values = [0]
                alert.operator = '>='

            alert.category = category.value
            alert.category_key = category.name
            alert.description = "Alert-" + str(uuid.uuid4())
            alert.fields = self.fields_for_ui(category.name, values)
            alerts.append(alert)
        return alerts


    def jvm_alerts(self):
        return list(filter(lambda element: element.category_key.startswith("jvm"), self.all_alerts()))

    def web_sessions_alerts(self):
        return list(filter(lambda element: element.category_key.startswith("web_sessions"), self.all_alerts()))

    def eap_transactions_alerts(self):
        return list(filter(lambda element: element.category_key.startswith("eap_transactions"), self.all_alerts()))

    def messaging_alerts(self):
        return list(filter(lambda element: element.category_key.startswith("messaging"), self.all_alerts()))

    def datasource_alerts(self):
        return list(filter(lambda element: element.category_key.startswith("datasource"), self.all_alerts()))