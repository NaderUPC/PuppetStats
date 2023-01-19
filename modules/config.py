import yaml


config = yaml.safe_load(open("config.yaml"))

url = config["url"]
username = config["username"]
password = config["password"]