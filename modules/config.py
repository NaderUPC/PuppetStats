import yaml


config = yaml.safe_load(open("config.yaml"))

class puppet:
    url = config["puppet"]["url"]
    username = config["puppet"]["username"]
    password = config["puppet"]["password"]

class influxdb:
    server = config["influxdb"]["server"]
    db = config["influxdb"]["db"]
