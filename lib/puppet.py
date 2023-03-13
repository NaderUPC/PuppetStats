import simplejson
import lib.apibase as apibase


class Puppet(apibase.API):
    def __init__(self, url: str, username: str, password: str) -> None:
        super().__init__(url, username, password)
    
    
    def hosts(self,
              location: str = "",
              group: str = "",
              hostname: str = "",
              reboot: bool = False,
              autoreboot: bool = False,
              security_updates: bool = False,
              esm: bool = False) -> list:
        # Global options
        uri = "api/hosts"
        params = { "per_page": "all" }
        if location and not group:
            params["search"] = f"{location}"
        if not location and group:
            params["search"] = f"parent_hostgroup={group}"
        if location and group:
            params["search"] = f"{location} and parent_hostgroup={group}"
        
        # Mode selection
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
        elif esm:
            params["search"] += " facts.ua_valid_until !~ ''"
        
        # HTTP GET response
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
        
        if os[0] == "Windows":
            win_kern_ver = os[1].split('.')
            if win_kern_ver[0] == "6":
                if win_kern_ver[1] == "0":
                    os[1] = "2008"
                elif win_kern_ver[1] == "1":
                    os[1] = "2008 R2"
                elif win_kern_ver[1] == "2":
                    os[1] = "2012"
                elif win_kern_ver[1] == "3":
                    os[1] = "2012 R2"
            elif win_kern_ver[0] == "10":
                if win_kern_ver[2] == "14393":
                    os[1] = "2016"
                elif win_kern_ver[2] == "17763":
                    os[1] = "2019"
                elif win_kern_ver[2] == "20348":
                    os[1] = "2022"
            del win_kern_ver
        elif os[0] == "RedHat" or os[0] == "Ubuntu": pass
        else: os[1] = os[1].split('.')[0]
        
        return ' '.join(os)
