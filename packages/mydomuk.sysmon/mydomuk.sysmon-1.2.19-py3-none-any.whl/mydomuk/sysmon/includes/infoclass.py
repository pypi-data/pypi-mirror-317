from .logger import infolog
import re

class InfoClass:
    def update(self, key: str, value, prefix: str) -> None:
        key = key.lower()
        key.startswith(prefix)
        if key.startswith(prefix) is False:
            return False

        key = key[len(prefix):]

        if len(value) > 2:
            if value[0] == "\"" and value[-1] == "\"":
                value = value[1:-1]

        if value is None or len(str(value)) == 0:
            return False

        if hasattr(self, key):
            cur = getattr(self, key)
            if type(cur) is int:
                setattr(self, key, int(value))
            elif type(cur) is bool:
                if value == 0 or str(value).lower()[0] == "f" or str(value).lower()[0] == "n":
                    setattr(self, key, False)
                else:
                    setattr(self, key, True)
            else:
                setattr(self, key, value)

        return True
    
    def amend_hostnames(self, hostname: str, vip_hostname: str = None):
        hostname_pattern: str = "{{ *hostname *}}"
        vip_pattern: str = "{{ viphost *}}"
        for key in self.__dict__.keys():
            value = getattr(self, key)
            if isinstance(value, str):
                newvalue = re.sub(hostname_pattern,  hostname, value, flags=re.IGNORECASE)
                if newvalue != value:
                    infolog(f"Updating Hostname in {self.__class__.__name__}.{key} from '{value}' to '{newvalue}'")
                    setattr(self, key, newvalue)
                    value = newvalue
                if vip_hostname is not None:
                    newvalue = re.sub(vip_pattern,  vip_hostname, value, flags=re.IGNORECASE)
                    if newvalue != value:
                        infolog(f"Updating VIP Hostname in {self.__class__.__name__}.{key} from '{value}' to '{newvalue}'")
                        setattr(self, key, newvalue)                    
