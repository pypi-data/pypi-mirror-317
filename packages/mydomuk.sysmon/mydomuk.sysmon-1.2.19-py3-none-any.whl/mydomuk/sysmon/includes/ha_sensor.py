from typing import TYPE_CHECKING, Callable
import psutil
from datetime import datetime, timezone
from .logger import infolog, debuglog, errorlog
from .constants import *
from socket import AddressFamily
import paho.mqtt.client as mqtt
from .sensor_stats import SensorStats
from .sensors import Sensor

if TYPE_CHECKING:
    from .ha_device import HomeAssistantDevice


class HomeAssistantSensor:
    '''
    Home Assistant Sensor Class

    A HA Sensor relates to an HA Entity subordinate to an HA Device

    '''
    def __init__(
            self,
            sensor: Sensor,
            device: "HomeAssistantDevice") -> None:
        self.name: str = sensor.name
        self.state_topic: str = None
        self.device_class: str = sensor.device_class
        self.state_class: str = sensor.state_class
        self.value_template: str = None
        self.uid_suffix: str = None
        self._uidsuffix: str = sensor.id
        self.unique_id: str = None
        self.availability_topic: str = None
        self.device: HomeAssistantDevice = device
        self.unit_of_measurement: str = sensor.unit
        self.retain: bool = sensor.retain
        self.value_function: callable = sensor.value_function
        self.value = None
        self.fn_parms: any  = sensor.fn_parms
        self.isvip: bool = sensor.isvip
        self.isavailability: bool = sensor.isavailability
        self.sendsolo: bool = sensor.sendsolo
        self.windows_only: bool = sensor.windows_only
        self.non_windows_only: bool = sensor.non_windows_only

        self.update_suffix(sensor.id)
        # if sensor.isnic:
        #     self.value_function = self.get_nic_addr
        # elif sensor.isvip:
        #     self.value_function = self.get_vip_addr
        #     self.retain = True
        

    @classmethod
    def firstrun(cls):
        SensorStats.get_stats()

    def update_suffix(self, uidsuffix):
        self.uid_suffix = uidsuffix
        self.unique_id = self.device.uid + "_" + uidsuffix

    def discovery_data(self) -> dict:
        obj = {"name": self.name,
               "state_topic": self.state_topic,
               "unique_id": self.unique_id,
               "object_id": self.unique_id,
               "device": self.device.json()
              }
        if self.device_class is not None:
            obj["device_class"] = self.device_class
        if self.value_template is not None:
            obj['value_template'] = self.value_template
        if self.sendsolo is False:
            obj['value_template'] = "{{ value_json['" + self.uid_suffix + "'] }}"
        if self.availability_topic is not None:
            obj["payload_available"] = "online"
            obj["payload_not_available"] = "offline"
            obj['availability_topic'] = self.availability_topic
        if self.unit_of_measurement is not None:
            obj['unit_of_measurement'] = self.unit_of_measurement
        if self.state_class is not None:
            obj['state_class'] = self.state_class
        return obj

    def get_value(self):
        if self.fn_parms is None:
            return self.value_function()
        else:
            return self.value_function(self.fn_parms)
