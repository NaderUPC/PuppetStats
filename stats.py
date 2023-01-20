#!/usr/bin/env python3

import modules.influxdb as influxdb
import modules.puppet as puppet
import modules.config as config
from datetime import datetime


def main():
    # === InfluxDB & Puppet setup === #
    timestamp = datetime.now()
    db = influxdb.InfluxDB(config.influxdb.server, config.influxdb.db, timestamp)
    db_client = db.setup_db()
    puppet = puppet.Puppet(config.puppet.url, config.puppet.username, config.puppet.password)
    
    ##


if __name__ == "__main__":
    main()
