from datetime import timezone

SYSMON_VERSION = "1.2.18"               # Current version of Sysmon
DEGREE_SIGN = u'\u2103'                 # Used to put out the temperature measurement unit
RUN_LOOP_HOUR = 3600                    # Interval before issuing still here message
MQTT_MULTI_TOPIC_NODE = "raw"           # Topic suffix to use for JSON data in the bulk MQTT sensor data
MQTT_MESSAGE_EXPIRY_SECONDS = 7200      # Expire after 2 hours, we will republish every hour if using version 5
MQTT_SUBSCRIBE_DELAY_WAIT = 0.1         # Initial delay before checking for Subscription messages
MQTT_SUBSCRIBE_INTERVAL_WAIT = 0.05     # Interval to wait when found the same number of subscriptions
MQTT_SUBSCRIBE_MAX_WAIT_TIME = 10       # Maximum time to wait for all Subscription messages to arrive
MQTT_SUBSCRIBE_MAX_DUPLICATES = 5       # Maximum number of times we can see the same number of Subscription messages before assuming all have arrived
STORE_TRUE = "store_true"               # String for use with argparse
UTC = timezone.utc                      # Timezone to send timestamps with
