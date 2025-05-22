import configparser



config = configparser.ConfigParser()
config.read("conf.conf")


web_site_host = config["site"]["HOST"]
web_site_port = config["site"]["PORT"]



HOST = config["database"]["HOST"]
PORT = config["database"]["PORT"]
USERNAME = config["database"]["USERNAME"]
PASSWORD = config["database"]["PASSWORD"]
DMNAME = config["database"]["DBNAME"]


