from enum import Enum

class AlertCategory(Enum):

    # Datasource Alerts
    datasource_connection_creation_time = 'DataSource - Connection Creation Time'
    datasource_connection_get_time = 'DataSource - Connection Get Time'
    datasource_connection_wait_time = 'DataSource - Connection Wait Time'
    datasource_connections_available = 'DataSource - Connections Available'
    datasource_connections_in_use = 'DataSource - Connections In Use'
    datasource_connections_timeout = 'DataSource - Connections Time Out'

    # EAP Alerts
    eap_transactions_aborted = 'EAP Transactions - Aborted'
    eap_transactions_application_rollback = 'EAP Transactions - Application Rollbacks'
    eap_transactions_committed = 'EAP Transactions - Committed'
    eap_transactions_heuristic = 'EAP Transactions - Heuristic'
    eap_transactions_resource_rollback = 'EAP Transactions - Resource Rollbacks'
    eap_transactions_timed_out = 'EAP Transactions - Timed Out'


    # JVM
    jvm_accumulated_gc_duration = 'JVM Accumulated GC Duration'
    jvm_heap_used = 'JVM Heap Used'
    jvm_non_heap_used = 'JVM Non Heap Used'


    # Messaging
    messaging_delivery_message_count = 'Messaging - Delivering Message Count'
    messaging_durable_message_count = 'Messaging - Durable Message Count'
    messaging_durable_subscribers = 'Messaging - Durable Subscribers'
    messaging_messages_added = 'Messaging - Messages Added'
    messaging_messages_count = 'Messaging - Messages Count'
    messaging_non_durable_message_count = 'Messaging - Non-durable Message Count'
    messaging_non_durable_subscribers = 'Messaging - Non-durable Subscribers'
    messaging_subscriptions = 'Messaging - Subscriptions'


    # Web sessions
    web_sessions_active = 'Web sessions - Active'
    web_sessions_expired = 'Web sessions - Expired'
    web_sessions_rejected = 'Web sessions - Rejected'

    @staticmethod
    def list():
        return map(lambda c: c.value, AlertCategory)