import lib.influxdb as influxdb
import lib.puppet as puppet

groups = ["UPCnet/" + group for group in ["SO", "IE"]]


def os(db_ep: influxdb.InfluxDB, puppet_ep: puppet.Puppet) -> list:
    payloads = []
    # Tauli
    payloads.append(db_ep.os(
        location = "Tauli",
        group = "",
        hosts = puppet_ep.hosts(location = "Tauli")
    ))
    # UPC
    for group in groups:
        payloads.append(db_ep.os(
            location = "UPC",
            group = group,
            hosts = puppet_ep.hosts(location = "UPC", group = group)
        ))
    return payloads


def security(db_ep: influxdb.InfluxDB, puppet_ep: puppet.Puppet) -> list:
    payloads = []
    for group in groups:
        payloads.append(db_ep.security(
            group = group,
            hosts = puppet_ep.hosts(group = group),
            puppet_ep = puppet_ep
        ))
    return payloads


def esm(db_ep: influxdb.InfluxDB, puppet_ep: puppet.Puppet) -> list:
    payloads = []
    for group in groups:
        payloads.append(db_ep.esm(
            group = group,
            hosts = puppet_ep.hosts(group = group)
        ))
    return payloads


def reboot(db_ep: influxdb.InfluxDB, puppet_ep: puppet.Puppet) -> list:
    payloads = []
    for group in groups:
        payloads.append(db_ep.reboot(
            group = group,
            reboot_hosts = puppet_ep.hosts(group = group, reboot = True),
            autoreboot_hosts = puppet_ep.hosts(group = group, autoreboot = True)
        ))
    return payloads
