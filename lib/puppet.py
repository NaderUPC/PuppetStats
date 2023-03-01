import simplejson
import lib.apibase as apibase


class Puppet(apibase.API):
    def __init__(self, url: str, username: str, password: str) -> None:
        super().__init__(url, username, password)
    
    
    def hosts(self, location: str = "", group: str = "", reboot: bool = False, autoreboot: bool = False, security_updates: bool = False, hostname: str = "") -> list:
        uri = "api/hosts"
        params = { "per_page": "all" }
        if location and not group:
            params["search"] = f"{location}"
        if not location and group:
            params["search"] = f"parent_hostgroup={group}"
        if location and group:
            params["search"] = f"{location} and parent_hostgroup={group}"
        
        if reboot:
            params["search"] += " and facts.apt_reboot_required=true"
        elif autoreboot:
            uri = "api/smart_class_parameters/3320/override_values"
            params.pop("search")
            params["per_page"] = "500"
        elif security_updates:
            uri = f"api/hosts/{hostname}/facts"
            params["per_page"] = "1000"
            params["search"] = "apt_security_updates"
        
        r = self.get(uri, params = params)
        try:
            return r.json()["results"]
        except (simplejson.JSONDecodeError, KeyError):
            raise self.NotAvailableError(r.status_code)
    
    
    def facts_of(self, hostname: str) -> dict:
        params = { "per_page": "1000" }
        r = self.get(f"api/hosts/{hostname}/facts", params = params)
        try:
            return r.json()["results"][hostname]
        except (simplejson.JSONDecodeError, KeyError):
            raise self.NotAvailableError(r.status_code)
    
    
    @staticmethod
    def os(host: dict) -> str:
        os = host["operatingsystem_name"].split()
        
        if os[0] == "windows": os[0] = "Windows"
        if os[0] == "RHEL": os[0] = "RedHat"
        if os[0] == "RedHat" and len(os) == 3: os.pop(1)
        if os[0] == "CentOS" and len(os) == 3: os.pop(1)
        if os[0] == "Ubuntu" and len(os) == 3: os.pop(2)
        if os[0] == "SUSE":
            for _ in range(3): os.pop(1)
        if os[0] == "SLES":
            os[0] = "SUSE"
            if len(os) == 3: os.pop(2)
        if os[0] == "Oracle":
            os[0] = "OracleLinux"
            for _ in range(3): os.pop(1)
        
        os[1] = os[1].split('.')[0]
        return ' '.join(os)
