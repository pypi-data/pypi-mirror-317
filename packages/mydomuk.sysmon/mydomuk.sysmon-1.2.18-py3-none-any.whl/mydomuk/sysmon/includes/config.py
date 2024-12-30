from importlib import resources
from os import path as os_path
from .mqttinfo import MQTTInfo
from .ha_info import HomeAssistantInfo
from argparse import ArgumentParser, Namespace
from .constants import STORE_TRUE
from .tools import gethostname
from .sensor_stats import SensorStats


class Config:
    def __init__(self, args: Namespace) -> None:
        self.source: str = args.source
        self.host: str = args.host
        self.port: int = args.port
        self.user: str = args.user
        self.password: str = args.password
        self.createsource: bool = args.createsource
        self.debug: bool = args.debug
        self.verbose: bool = args.verbose
        self.reset_discovery: bool = args.reset_discovery
        self.sleep: float = args.sleep
        self.loop: int = args.loop
        self.printresults: bool = args.printresults
        self.printtime: bool = args.printtime
        self.finalrun: bool = False
        self.runloop: bool = False if args.no_run_loop else True
        self.dryrun: bool = args.dryrun
        self.hostname: str = gethostname() if args.hostname is None else args.hostname
        SensorStats.hostname = self.hostname


    @classmethod
    def get_command_line_args(cls) -> "Config":
        parser = ArgumentParser(prog="sysmon")
        parser.add_argument("-src",dest="source", help="Configuration File Containing Environment Type entries, use -cs to generate example")
        parser.add_argument("-host", dest="host", help="MQTT Host")
        parser.add_argument("-port", dest="port", type=int, default=1883, help="MQTT port")
        parser.add_argument("-user", dest="user", help="MQTT User")
        parser.add_argument("-pass", dest="password", help="MQTT password")
        parser.add_argument("-cs", dest="createsource", action=STORE_TRUE, help="Create empty source configuration")
        parser.add_argument("-hn", dest="hostname", help="Override the hostname")
        parser.add_argument("-d", dest="debug", action=STORE_TRUE, help="Enable debug logging")
        parser.add_argument("-v", dest="verbose", action=STORE_TRUE, help="Enable verbose logging, debug included!")
        parser.add_argument("-rd", dest="reset_discovery", action=STORE_TRUE, help="Reset discovery information for this host")
        parser.add_argument("-s",dest="sleep", type=float, default=30, help="Seconds to sleep between loops, defaults to 30")
        parser.add_argument("-l",dest="loop", type=int, default=0, help="Number of loops to do, defaults to 0 implying infinite")
        parser.add_argument("-pr", dest="printresults", action=STORE_TRUE, default=False, help="Print sensor values at each loop")
        parser.add_argument("-nrl", dest="no_run_loop", action=STORE_TRUE, help="Set this to prevent the loop running even once!")
        parser.add_argument("-dr", dest="dryrun", action=STORE_TRUE, help="Do all but send MQTT messages")

        parser.add_argument("-pt", dest="printtime", action="store_true", default=False, help="Print timestamp at each loop")
        args = parser.parse_args()
        return Config(args)


    @classmethod
    def print_example_source_file(cls):
        print("# Configuration File save this as a .src file and edit it")
        print("# ************** START ********************")
        try:
            import mydomuk.sysmon.resources as mydomresources
            print(resources.files(mydomresources).joinpath("example.src").read_text(encoding="UTF-8"))
        except ImportError:
            curpath = os_path.dirname(__file__)
            example = os_path.join(curpath, "resources", "example.src")
            with open(example, encoding="UTF-8", mode="rt") as ef:
                print(ef.read())
        print("# ************** ENDS  ********************")    
        
    def load_configuration_settings(self) -> tuple[MQTTInfo, HomeAssistantInfo]:
        '''
        Load a Source File for Configuration Variables and apply cli settings after
        '''
        mqtti = MQTTInfo()
        hass = HomeAssistantInfo()
        if self.source is not None and os_path.exists(self.source):
            with open(self.source, "rt", encoding="UTF-8") as file_no:
                lines = file_no.readlines()
                for line in lines:
                    line = line.strip()
                    if len(line) <= 0:
                        continue
                    if line[0] == "#":
                        continue
                    if " #"  in line:
                        idx = line.index(" #")
                        line = line[:idx].rstrip()
                    elements = line.split("=",1)
                    if len(elements) != 2:
                        continue
                    name, value = elements
                    if mqtti.update(name, value, "mqtt_") is True:
                        continue
                    if hass.update(name, value, "hass_") is True:
                        continue
        if self.host:
            mqtti.broker = self.host
        if self.port:
            mqtti.port = self.port
        if self.user:
            mqtti.user = self.user
        if self.password:
            mqtti.password = self.password
                
        mqtti.dryrun = self.dryrun

        hass.hostname = self.hostname
        mqtti.hostname = self.hostname
        hass.reset_discovery = self.reset_discovery

        return mqtti, hass
