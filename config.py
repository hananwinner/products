import yaml

with open("config/config.yaml", "r") as fdr:
    config = yaml.load(fdr)

consumer_config = config["consumer"]
mongo_config = config["mongo"]
