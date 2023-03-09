#!/usr/bin/env python3

import lib.influxdb as influxdb
import lib.puppet as puppet
import modules.config as config
import modules.funcs as funcs
from datetime import datetime

# from pprint import pprint  # DEBUG


def main():
    # === InfluxDB & Puppet Endpoints/Clients Setup === #
    timestamp = datetime.now()
    db_ep = influxdb.InfluxDB(config.influxdb.server, config.influxdb.db, timestamp)
    db_client = db_ep.setup_db()
    puppet_ep = puppet.Puppet(config.puppet.url, config.puppet.username, config.puppet.password)
    
    # === Payload === #
    payload = []
    # OS
    payload.extend(funcs.os(db_ep, puppet_ep))
    # Security
    payload.extend(funcs.security(db_ep, puppet_ep))
    # ESM
    payload.extend(funcs.esm(db_ep, puppet_ep))
    # Reboot
    payload.extend(funcs.reboot(db_ep, puppet_ep))

    # pprint(payload)  # DEBUG
    
    try: db_client.write_points(payload)
    except influxdb.exceptions.InfluxDBClientError: pass


if __name__ == "__main__":
    main()
