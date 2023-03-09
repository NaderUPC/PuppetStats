import lib.puppet as puppet
from influxdb import InfluxDBClient, exceptions
from datetime import datetime


class InfluxDB:
    def __init__(self, server: str, db: str, timestamp: datetime) -> None:
        self.server = server
        self.db = db
        self.timestamp = timestamp
    
    
    def setup_db(self) -> InfluxDBClient:
        client = InfluxDBClient(self.server)
        client.switch_database(self.db)
        return client
    
    
    def os(self, location: str, group: str, hosts: list) -> dict:
        if location == "Tauli":
            tags = { "location": location }
        elif location == "UPC":
            if group != "UPCnet/SO" and group != "UPCnet/IE":
                raise ValueError("group must be either UPCnet/SO or UPCnet/IE")
            else: tags = { "location": location, "group": group }
        else: raise ValueError("location must be either UPC or Tauli")
        
        os_values = {}
        for host in hosts:
            os = puppet.Puppet.os(host)
            os_values[os] = os_values.get(os, 0) + 1
        
        return {
            "measurement": "os",
            "tags": tags,
            "fields": os_values,
            "time": self.timestamp
        }
    
    
    def security(self, group: str, hosts: list, puppet_ep: puppet.Puppet) -> dict:
        if group != "UPCnet/SO" and group != "UPCnet/IE":
            raise ValueError("group must be either UPCnet/SO or UPCnet/IE")
        
        security_values = {}
        for host in hosts:
            hostname = host["name"]
            try: updates = int(puppet_ep.hosts(security_updates = True, hostname = hostname)[hostname]["apt_security_updates"])
            except KeyError: continue
            security_values[hostname] = updates
        
        return {
            "measurement": "security",
            "tags": { "group": group },
            "fields": security_values,
            "time": self.timestamp
        }
    
    
    def esm(self, group: str, hosts: list) -> dict:
        if group != "UPCnet/SO" and group != "UPCnet/IE":
            raise ValueError("group must be either UPCnet/SO or UPCnet/IE")
        
        esm_values = {}
        for host in hosts:
            os = puppet.Puppet.os(host)
            if os == "Ubuntu 20.04 LTS": continue
            esm_values[os] = esm_values.get(os, 0) + 1
        
        return {
            "measurement": "esm",
            "tags": { "group": group },
            "fields": esm_values,
            "time": self.timestamp
        }
    
    
    def reboot(self, group: str, reboot_hosts: list, autoreboot_hosts: list) -> dict:
        if group != "UPCnet/SO" and group != "UPCnet/IE":
            raise ValueError("group must be either UPCnet/SO or UPCnet/IE")
        
        to_reboot = set()
        for host in reboot_hosts:
            if isinstance(host, str): continue
            hostname = host["name"]
            to_reboot.add(hostname)
        
        autoreboot = set()
        for host in autoreboot_hosts:
            if isinstance(host, str): continue
            hostname = host["match"].split('=', maxsplit = 1)[1]
            autoreboot.add(hostname)
        
        EXCLUDED = {
            "adriana.upc.edu",
            "alcide.upc.edu",
            "amabella.upc.edu",
            "amalia1.upc.edu",
            "amalia2.upc.edu",
            "britta.upc.edu",
            "cameron.upc.edu",
            "connell.upc.edu",
            "conrad.upc.edu",
            "crushing.upc.edu",
            "fring.upc.edu",
            "hanaryo1.upc.edu",
            "hawkings1.upc.edu",
            "horatio1.upc.edu",
            "horatio2.upc.edu",
            "hotch1.upc.edu",
            "hotch2.upc.edu",
            "house1.upc.edu",
            "house2.upc.edu",
            "hutch.upc.edu",
            "jenessa.upc.edu",
            "larraq.upc.edu",
            "madeline.upc.edu",
            "minghella.upc.edu",
            "tattiawna.upc.edu"
            "teyla.upc.edu",
            "tobias.upc.edu",
            "tripp.upc.edu",
            "varys.upcnet.es",
            "winter.upc.edu"
        }
        total = to_reboot - (autoreboot | EXCLUDED)
        
        return {
            "measurement": "reboot",
            "tags": { "group": group },
            "fields": { "value": len(total) },
            "time": self.timestamp
        }
