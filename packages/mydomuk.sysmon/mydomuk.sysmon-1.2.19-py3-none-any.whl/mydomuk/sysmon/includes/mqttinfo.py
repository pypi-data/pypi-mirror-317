from .infoclass import InfoClass
from .tools import isWindows
import paho.mqtt.client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.enums import CallbackAPIVersion, MQTTProtocolVersion

from .logger import infolog, errorlog, debuglog, verboselog, get_logging_level, LOGLEVEL
from .ha_sensor import HomeAssistantSensor
from .sensor_stats import SensorStats
from .ha_device import HomeAssistantDevice
from .ha_info import HomeAssistantInfo
from .constants import *
from .sensors import Sensor, SENSORS
import json


class MQTTInfo(InfoClass):
    '''
    MQTT Info Class
    '''
    def __init__(self) -> None:
        self.broker: str = None
        self.port: int = 1883
        self.user: str = None
        self.password: str = None
        self.ssl: bool = False
        self.cacert: str = None
        self.insecure: bool = False
        self.topic_prefix: str = "MyDomUK"
        self.device_topic: str = "sysmon/{{hostname}}"
        self.protocol_version_5: bool = True
        self.vip_host: str = None
        self.vip_topic: str = None
        self.vip_monit: str = None
        self.nic_monit: str = None
        self.disk_monit: str = None
        self.connected: bool = False
        self.client: mqtt.Client = None
        self.hostname: str = None
        self._device: HomeAssistantDevice = None
        self._vipdevice: HomeAssistantDevice = None
        self._sensors: list[HomeAssistantSensor] = []
        self._hass: HomeAssistantInfo = None
        self._state_sensor: HomeAssistantSensor = None
        self.topic_callbacks: dict[str, list] = {}
        self.dryrun: bool = False

    def initialise(self, hass: HomeAssistantInfo):
        self._hass = hass
        devicename = hass.device
        deviceid = hass.deviceid
        self._device = HomeAssistantDevice(devicename, deviceid)
        self._device.manufacturer = hass.manufacturer
        self._device.model = hass.model

        if self.vip_host is None:
            self.vip_host = "virtualcluster"

        self._vipdevice = HomeAssistantDevice(
            devicename.replace(self.hostname, self.vip_host), deviceid.replace(self.hostname, self.vip_host))
        self._vipdevice.manufacturer = "Virtual"
        self._vipdevice.model = "VRRP"

    def get_state_sensor_topic(self) -> str:
        return self._state_sensor.state_topic

    def make_ha_sensor(self, sensor: Sensor) -> HomeAssistantSensor:
        device: HomeAssistantDevice = self._device if sensor.isvip is False else self._vipdevice
        ha_sensor = HomeAssistantSensor(sensor, device)
        self._sensors.append(ha_sensor)
        return ha_sensor

    def make_sensors(self):
        infolog("Creating HomeAssistant Sensors")
        windows: bool = isWindows()
        # sensor: HomeAssistantSensor = None
        state_sensor: HomeAssistantSensor = None
        for sensor in SENSORS:
            ha_sensor = self.make_ha_sensor(sensor)
            if ha_sensor.isavailability:
                state_sensor = ha_sensor
                self._state_sensor = ha_sensor

        if self.disk_monit is not None:
            for disk in self.disk_monit.split(" "):
                name, _, mountpoint = disk.partition(",")
                name = name.strip()
                mountpoint = mountpoint.strip()
                sensor = Sensor(name=f"{name} FS Usage", value_function=SensorStats.get_disk_usage, fn_parms=mountpoint, unit="%", measurement=True)
                self.make_ha_sensor(sensor)

        if self.nic_monit is not None:
            for nic in self.nic_monit.split(","):
                nic = nic.strip()
                sensor = Sensor(name=f"NIC {nic}", isnic=True, value_function=SensorStats.get_nic_addr, fn_parms=nic)
                self.make_ha_sensor(sensor)

        if self.vip_monit is not None:
            for vip in self.vip_monit.split(","):
                vip = vip.strip()
                safevip = vip.lower().replace(" ", "_").replace(".", "")
                sensor = Sensor(name=f"VIP {vip}", id=f"vip_{safevip}", isvip=True, sendsolo=True, value_function=SensorStats.get_vip_addr, fn_parms=vip, retain=True)
                ha_sensor = self.make_ha_sensor(sensor)
                ha_sensor.state_topic = self.make_vip_topic(safevip)

        for ha_sensor in self._sensors:
            if ha_sensor.isvip is False:
                ha_sensor.state_topic = self.make_sensor_topic(ha_sensor.uid_suffix, ha_sensor.sendsolo)
                if ha_sensor.isavailability is False:
                    ha_sensor.availability_topic = self.make_sensor_topic(
                        state_sensor.uid_suffix, True
                    )


    def validate_settings(self) -> None:
        '''
        Validate MQTTInfo settings and raises ValueErrors if incorrect
        '''
        self.amend_hostnames(self.hostname, self.vip_host)
        if self.device_topic is None:
            raise ValueError("Missing MQTT_DEVICE_TOPIC")
        if self.topic_prefix is None:
            raise ValueError("Missing MQTT_TOPIC_PREFIX")
        if self.broker is None:
            raise ValueError("Missing MQTT_BROKER, hostname or IP address required")

    def get_topic(self, suffix: str) -> str:
        return self.topic_prefix + "/" + suffix

    def make_sensor_topic(self, sensor_suffix: str, sendsolo: bool) -> str:
        if sendsolo:
            return self.get_topic(self.device_topic + "/" + sensor_suffix)
        else:
            return self.make_bulk_topic()

    def make_bulk_topic(self):
        return self.get_topic(self.device_topic + "/" + MQTT_MULTI_TOPIC_NODE)

    def make_vip_topic(self, vip_suffix: str) -> str:
        # safevip: str = vip_suffix.replace(".","")
        return self.get_topic(self.vip_topic + "/" + vip_suffix)

    def connect_broker(
            self,
            will_topic: str = None,
            will_message: str= None) -> None:
        infolog(f"Connecting to MQTT Broker : {self.broker} with user {self.user}")
        protocol: MQTTProtocolVersion = mqtt.MQTTv5 if self.protocol_version_5 else mqtt.MQTTv311
        self.client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=protocol,
                                reconnect_on_failure=True)
        self.client.on_connect_fail = self.on_mqtt_connect_fail
        self.client.on_disconnect = self.on_mqtt_disconnect
        self.client.on_message = self.on_mqtt_message
        if self.user is not None:
            self.client.username_pw_set(self.user, self.password)
        if self.ssl:
            self.client.tls_set()
        if self.cacert is not None:
            self.client.tls_set(ca_certs=self.cacert)
            self.client.tls_insecure_set(True)
        if will_message is not None and will_topic is not None:
            self.client.will_set(will_topic, will_message, retain=True)
        try:
            ec = self.client.connect(host=self.broker, port=self.port)
            if ec == 0:
                infolog(f"MQTT Connection Established to Broker : {self.broker}")
                self.client.loop_start()
                self.connected = True
                
            else:
                infolog(f"Broker Connect Error Code : {ec}")
                self.connected = True
        except Exception as e:
            self.connected = False
            infolog(f"Broker Connect Failed : {e}")
        return self.connected

    def subscribe(self, topic: str, callback: callable = None, mustmatch: str = None):
        if callback is not None:
            if topic.endswith("#"):
                subtopic: str = topic[0:-1]
            else:
                subtopic: str = topic
            if subtopic not in self.topic_callbacks:
                self.topic_callbacks[subtopic] = []
            self.topic_callbacks[subtopic].append((callback, mustmatch))
        self.client.subscribe(topic)

    def unsubscribe(self, topic: str) -> None:
        self.client.unsubscribe(topic)

    def sensors(self) -> "list[HomeAssistantSensor]":
        return list(self._sensors)

    def send_ha_discovery(self, quiet: bool):
        hass = self._hass
        if hass.discovery:
            hass.send_discoveries(self, self.topic_prefix, quiet=quiet)


    def on_mqtt_connect_fail(self, client: any, userdata: any, flags: any, rc: any):
        ''' On MQTT Failure '''
        self.connected = False
        errorlog(f"MQTT Connect Failed to Broker : {self.broker}")
        errorlog(f"User Data : {userdata}")
        errorlog(f"Flags : {flags}")
        errorlog(f"RC : {rc}")


    def on_mqtt_disconnect(self, client: any, userdata: any, disconnect_flags, rc: any, properties):
        self.connected = False
        infolog(f"MQTT Disconnect - {rc}")

    def on_mqtt_message(self, mqttc, obj, msg):
        msg_topic: str = msg.topic
        debuglog(f"Received : {msg_topic}")
        for topic, callbacks in self.topic_callbacks.items():
            if msg_topic.startswith(topic):
                for callback, mustmatch in callbacks:
                    callback(self, msg_topic, msg.qos, msg.payload, mustmatch)


    def send_all_sensors_updates(self, printresults: bool):
        sendqueue: list[tuple] = []
        blob = {}
        HomeAssistantSensor.firstrun()
        bulktopic: str = self.make_bulk_topic()
        for sensor in self.sensors():
            if sensor is None:
                continue
            message = sensor.get_value()
            if message is None and sensor.isvip:
                break
            if printresults:
                infolog(f"{sensor.name:16s} : {message}")
            if sensor.sendsolo:
                sendqueue.append((sensor.state_topic, message, sensor.retain))
            else:
                blob[sensor.uid_suffix] = message

        blobdata = json.dumps(blob)
        sendqueue.append((bulktopic, blobdata, False))
        for topic, data, retain in sendqueue:
            self.send_mqtt(topic=topic, message=data, retain=retain)


    def send_mqtt(
            self,
            topic:str,
            message:str,
            retain: bool = False,
            isHAdiscovery: bool = False,
            retained_expiry_seconds: int = 0,
            retries: int = 3,
            timeout: int = 1) -> bool:
        ''' 
        Send an MQTT Message 
        '''
        sent: bool = False
        errprefix: str = "MQTT Send"
        props: mqtt.Properties = None
        if retain and retained_expiry_seconds > 0 and self.protocol_version_5:
            try:
                props = mqtt.Properties(PacketTypes.PUBLISH)
                props.MessageExpiryInterval=retained_expiry_seconds
            except Exception as e:
                print(f"Props Error : {e}")
        if isHAdiscovery:
            if message is None:
                errprefix = "HA Discovery Reset"
                message = ""
            else:
                errprefix = "HA Discovery Message"
        
        if self.dryrun is False:
            verboselog(f"Sending Topic : {topic}, Message : {message}, Retain : {retain}")
            while sent is False:                        
                response = self.client.publish(topic, message, retain=retain, properties=props)
                try:
                    response.wait_for_publish(timeout)
                    sent = True
                except ValueError:
                    retries -= 1
                    if retries > 0:
                        errorlog(f"{errprefix} for : {topic}, failed retrying")
                    else:
                        errorlog(f"{errprefix} for : {topic}, failed retry limit reached")
                        break
                except RuntimeError as er:
                    errorlog(f"{errprefix} for {topic}, fatal runtime error : {er}")
                    break
                except Exception as e:
                    errorlog(f"{errprefix} for {topic}, fatal error : {e}")
                    break
        else:
            if get_logging_level() == LOGLEVEL.LEVEL_VERBOSE:
                verboselog(f"DRYRUN : Would Send Topic:{topic}, Retain:{retain}, Message:{message}")
            else:
                infolog(f"DRYRUN : Would Send Topic:{topic}, Retain:{retain}")
            sent = True
        return sent

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
        self.client = None
