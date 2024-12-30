from .infoclass import InfoClass
from .logger import infolog, errorlog, isDebug, debuglog, warnlog
import json
from typing import TYPE_CHECKING
from time import sleep, time
from .constants import MQTT_MESSAGE_EXPIRY_SECONDS, MQTT_SUBSCRIBE_DELAY_WAIT, MQTT_SUBSCRIBE_INTERVAL_WAIT, MQTT_SUBSCRIBE_MAX_DUPLICATES, MQTT_SUBSCRIBE_MAX_WAIT_TIME
from threading import Lock
if TYPE_CHECKING:
    from .mqttinfo import MQTTInfo


class HomeAssistantInfo(InfoClass):
    '''
    Home Assistant Information Class

    This class holds the user supplied information for communication with HomeAssistant
    '''
    def __init__(self) -> None:
        self.discovery: bool = False
        self.topic_prefix: str = "homeassistant"
        self.manufacturer: str = None
        self.model: str = None
        self.device: str = None
        self.deviceid: str = None
        self.vip_device: str = None
        self.vip_deviceid: str = None
        self.reset_discovery: bool = False
        self.reset_topics: list[str] = []
        self.serial_lock: Lock = Lock()
        self.hostname: str = None
        self.alt_hostname: str = None

    def validate_settings(self) -> None:
        '''
        Validate HomeAssistant settings and raises ValueErrors if incorrect
        '''
        self.vip_device = self.device
        self.vip_deviceid = self.deviceid
        self.amend_hostnames(self.hostname, self.alt_hostname)
        if self.device is None:
            raise ValueError("Missing HASS_DEVICE - Device description required")
        if self.deviceid is None:
            raise ValueError("Missing HASS_DEVICEID - Unique device ID required")

    def reset_discoveries(self, mqtti: "MQTTInfo", prefix: str, delay_seconds: int) -> None:
        self.reset_discovery = False
        subscription: str = f"{self.topic_prefix}/sensor/{prefix}/#"
        mustmatch: str = f"{self.topic_prefix}/sensor/{prefix}/{mqtti._device.uid}"
        infolog(f"Listening for HomeAssistant topics on {self.topic_prefix}/sensor/{prefix}/#")
        infolog(f"Must Match : {mustmatch}")
        time_start = time()
        mqtti.subscribe(subscription, self.topic_callback, mustmatch)
        infolog(f"Waiting up to {MQTT_SUBSCRIBE_MAX_WAIT_TIME:.2f} seconds to received HomeAssistant Subscription messages")        
        topic_size: int = 0
        sleep(MQTT_SUBSCRIBE_DELAY_WAIT)
        dup_count: int = 0
        while True:
            elapsed_time = time() - time_start
            with self.serial_lock:
                new_topic_size: int = len(self.reset_topics)
            if elapsed_time > MQTT_SUBSCRIBE_MAX_WAIT_TIME:
                warnlog(f"Maximum wait time of {MQTT_SUBSCRIBE_MAX_WAIT_TIME} seconds exceeded waiting for all subscription messages to arrive, aborted!")
                break
            if new_topic_size == 0:
                pass
            elif new_topic_size != topic_size:
                dup_count = 0
                topic_size = new_topic_size
                debuglog(f"*** Found : {topic_size} messages so far in {elapsed_time:.2f} seconds ***")
            else:
                dup_count += 1
                if dup_count == MQTT_SUBSCRIBE_MAX_DUPLICATES:
                    debuglog(f"*** Found : {topic_size} messages again in {elapsed_time:.2f} seconds, aborted! ***")
                    break
            sleep(MQTT_SUBSCRIBE_INTERVAL_WAIT)
        infolog(f"Found : {topic_size} HomeAssistant Sysmon Subscriptions for {self.hostname} in {elapsed_time:.2f} seconds")
        mqtti.unsubscribe(subscription)
        with self.serial_lock:
            for topic in self.reset_topics:
                self.reset_ha_topic(mqtti, topic)
            infolog(f"HA Reset sent for {len(self.reset_topics)} HA discovery topics starting with {subscription}")

            self.reset_topics.clear()


    def topic_callback(self, mqtti: "MQTTInfo", topic: str, qos, payload, mustmatch: str):
        if topic.startswith(mustmatch):
            debuglog(f"HA Topic Received : {topic}")
            with self.serial_lock:
                self.reset_topics.append(topic)


    def reset_ha_topic(self, mqtti: "MQTTInfo", topic: str) -> None:
        infolog(f"Sending Reset for {topic}")
        mqtti.send_mqtt(topic, None, True, True)

    def send_discoveries(self,
                       mqtti: "MQTTInfo",
                       prefix: str,
                       quiet: bool):
        infolog(f"Sending HA Discoveries for Device : {self.device}")
        for sensor in mqtti.sensors():
            discovery_topic = f"{self.topic_prefix}/sensor/{prefix}/{sensor.unique_id}/config"
            if self.reset_discovery:
                # Reset the Discovery First, Just in case!
                if isDebug():
                    debuglog(f"Resetting HA Discovery for Sensor : {sensor.name} - {discovery_topic}")
                else:
                    if quiet is False:
                        infolog(f"Resetting HA Discovery for Sensor : {sensor.name}")
                mqtti.send_mqtt(discovery_topic, None, False, True)

            if isDebug():
                debuglog(
                    f"Sending HA Discovery for Sensor : {sensor.name} - {discovery_topic}")
            else:
                if quiet is False:
                    infolog(
                        f"Sending HA Discovery for Sensor : {sensor.name} - {sensor.unique_id}")
            retained_expiry_seconds: int = 0 if sensor.isavailability else MQTT_MESSAGE_EXPIRY_SECONDS
            mqtti.send_mqtt(discovery_topic, json.dumps(sensor.discovery_data()), True, True, retained_expiry_seconds=retained_expiry_seconds)

        # Only do the reset once!
        self.reset_discovery = False
