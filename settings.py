import configparser



config = configparser.ConfigParser()
config.read("conf.conf")






HOST = config["database"]["HOST"]
PORT = config["database"]["PORT"]
USERNAME = config["database"]["USERNAME"]
PASSWORD = config["database"]["PASSWORD"]
DMNAME = config["database"]["DBNAME"]


