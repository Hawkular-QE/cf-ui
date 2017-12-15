from enum import Enum

class AlertCategory(Enum):

    # Datasource Alerts
    datasource_connection_creation_time = ['mw_ds_average_creation_time', 'DataSource - Connection Creation Time']
    datasource_connection_get_time = ['mw_ds_average_get_time', 'DataSource - Connection Get Time']
    datasource_connection_wait_time = ['mw_ds_max_wait_time', 'DataSource - Connection Wait Time']
    datasource_connections_available = ['mw_ds_available_count', 'DataSource - Connections Available']
    datasource_connections_in_use = ['mw_ds_in_use_count', 'DataSource - Connections In Use']
    datasource_connections_timeout = ['mw_ds_timed_out', 'DataSource - Connections Time Out']

    # EAP Alerts
    eap_transactions_aborted = ['mw_tx_aborted', 'EAP Transactions - Aborted']
    eap_transactions_application_rollback = ['mw_tx_application_rollbacks', 'EAP Transactions - Application Rollbacks']
    eap_transactions_committed = ['mw_tx_committed', 'EAP Transactions - Committed']
    eap_transactions_heuristic = ['mw_tx_heuristics', 'EAP Transactions - Heuristic']
    eap_transactions_resource_rollback = ['mw_tx_resource_rollbacks', 'EAP Transactions - Resource Rollbacks']
    #eap_transactions_timed_out = ['mw_tx_timeout', 'EAP Transactions - Timed Out']


    # JVM
    jvm_accumulated_gc_duration = ['mw_accumulated_gc_duration', 'JVM Accumulated GC Duration']
    jvm_heap_used = ['mw_heap_used', 'JVM Heap Used']
    jvm_non_heap_used = ['mw_non_heap_used', 'JVM Non Heap Used']


    # Messaging
    messaging_delivery_message_count = ['mw_ms_topic_delivering_count', 'Messaging - Delivering Message Count']
    messaging_durable_message_count = ['mw_ms_topic_durable_message_count', 'Messaging - Durable Message Count']
    messaging_durable_subscribers = ['mw_ms_topic_durable_subscription_count', 'Messaging - Durable Subscribers']
    messaging_messages_added = ['mw_ms_topic_message_added', 'Messaging - Messages Added']
    messaging_messages_count = ['mw_ms_topic_message_count', 'Messaging - Messages Count']
    messaging_non_durable_message_count = ['mw_ms_topic_non_durable_message_count', 'Messaging - Non-durable Message Count']
    messaging_non_durable_subscribers = ['mw_ms_topic_non_durable_message_count', 'Messaging - Non-durable Subscribers']
    messaging_subscriptions = ['mw_ms_topic_non_durable_subscription_count', 'Messaging - Subscriptions']


    # Web sessions
    web_sessions_active = ['mw_aggregated_active_web_sessions', 'Web sessions - Active']
    web_sessions_expired = ['mw_aggregated_expired_web_sessions', 'Web sessions - Expired']
    web_sessions_rejected = ['mw_aggregated_rejected_web_sessions', 'Web sessions - Rejected']



    @staticmethod
    def list():
        return map(lambda c: c.value, AlertCategory)