import yaml


config = yaml.safe_load(open("config.yaml"))

puppet = {
    "url":      config["puppet"]["url"],
    "username": config["puppet"]["username"],
    "password": config["puppet"]["password"]
}
influxdb = {
    "server": config["influxdb"]["server"],
    "db":     config["influxdb"]["db"]
}
