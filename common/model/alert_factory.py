import uuid

from alert import Alert
from alert_category import AlertCategory


class AlertFactory:

    # Factory Method
    def create_alert(self, category):
        return Alert(category)

    def copy_for_edit(self, alert):
        return Alert(alert.category)

    # Create All Alerts Available
    def all_alerts(self):
        alerts = []
        for category in AlertCategory:
            alerts.append(self.create_alert(category))
        return alerts

    def jvm_alerts(self):
        return list(filter(lambda alert: alert.key().startswith("jvm"), self.all_alerts()))

    def web_sessions_alerts(self):
        return list(filter(lambda alert: alert.key().startswith("web_sessions"), self.all_alerts()))

    def eap_transactions_alerts(self):
        return list(filter(lambda alert: alert.key().startswith("eap_transactions"), self.all_alerts()))

    def messaging_alerts(self):
        return list(filter(lambda alert: alert.key().startswith("messaging"), self.all_alerts()))

    def datasource_alerts(self):
        return list(filter(lambda alert: alert.key().startswith("datasource"), self.all_alerts()))