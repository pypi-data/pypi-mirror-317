#!/usr/bin/env python3
'''
SysMon Module
'''
import atexit
from datetime import datetime
import time
from os import name as os_name
from sys import platform as sys_platform
from .includes.logger import initlog, infolog, debuglog, errorlog, LOGLEVEL
from .includes.mqttinfo import MQTTInfo
from .includes.tools import get_timestamp
from .includes.constants import *
from .includes.config import Config


initlog()

def exit_handler(mqtti: MQTTInfo, sensor_status_topic: str):
    infolog("Cleaning Up and Closing")
    if mqtti.connected:
        mqtti.send_mqtt(sensor_status_topic, "offline", True, timeout=5)


def set_logging_level(cfg: Config) -> None:
    if cfg.verbose:
        infolog("Changing LogLevel to Verbose")
        initlog(LOGLEVEL.LEVEL_VERBOSE)
    elif cfg.debug:
        infolog("Changing Loglevel to Debug")
        initlog(LOGLEVEL.LEVEL_DEBUG)


def main():
    '''
    Main Loop
    '''

    sensor_status_topic: str = None

    infolog(f"Sysmon Version {SYSMON_VERSION} running on {os_name} system {sys_platform}")

    cfg = Config.get_command_line_args()

    if cfg.createsource:
        Config.print_example_source_file()
        exit(0)

    set_logging_level(cfg)

    mqtti, hass = cfg.load_configuration_settings()

    mqtti.validate_settings()
    hass.validate_settings()

    mqtti.initialise(hass)

    if cfg.runloop:
        mqtti.make_sensors()
        sensor_status_topic = mqtti.get_state_sensor_topic()
        if mqtti.connected is False:
            mqtti.connect_broker(sensor_status_topic, "offline")
    else:
        if mqtti.connected is False:
            mqtti.connect_broker()

    if mqtti.connected:
        if hass.reset_discovery:
            hass.reset_discoveries(mqtti, mqtti.topic_prefix, 5)

    interval_start = datetime.now()
    send_discoveries: bool = False
    if cfg.runloop:
        if cfg.loop > 0:
            cfg.runloop = False                                     # Runloop now only if loop is 0 meaning permanent
        if mqtti.connected:
            atexit.register(exit_handler, mqtti, sensor_status_topic)
            mqtti.send_ha_discovery(quiet=False)
        infolog("Starting Monitor Loop")
        try:
            while True:
                interval_offset = datetime.now()
                interval_diff = interval_offset - interval_start
                if interval_diff.total_seconds() >= RUN_LOOP_HOUR:                   
                    infolog("Run loop still working")
                    interval_start = interval_offset
                    if mqtti.protocol_version_5:
                        send_discoveries = True
                debuglog(f"Performing Run Loop")

                if mqtti.broker:
                    if mqtti.connected is False:
                        mqtti.connect_broker(sensor_status_topic, "offline")

                    if mqtti.connected:
                        if send_discoveries:
                            mqtti.send_ha_discovery(quiet=True)
                            send_discoveries = False
                        
                        t = "Time"
                        if cfg.printresults or cfg.printtime:
                            infolog(f"{t:16s} : {get_timestamp()}")
                        # send_data(mqtti, cfg.printresults)
                        mqtti.send_all_sensors_updates(cfg.printresults)
                        if cfg.printresults:
                            infolog("*"*48)

                if cfg.runloop is False:                            #   Not infinite loop
                    cfg.loop = cfg.loop - 1
                    if cfg.loop < 1:
                        break

                if cfg.sleep > 0 and (cfg.runloop or cfg.loop > 0):
                    time.sleep(cfg.sleep)

            infolog("Monitor Loop Exited")
        except KeyboardInterrupt:
            infolog("Terminating due to user request")
        except Exception as e:
            errorlog(f"Terminating due to exception : {e}")
        
        if mqtti.connected:
            if sensor_status_topic is not None:
                infolog("Sending Offline")
                mqtti.send_mqtt(sensor_status_topic, "offline")

    mqtti.disconnect()

if __name__ == "__main__":
  main()
