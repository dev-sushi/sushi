"""
here sushi stores all variables that are used in multiple files
"""

import configparser

config = configparser.ConfigParser()
config.read("sushi.conf")

MULTIPLE_FILES = False
ONE_COMPILE = False

split_path = config["main"]["lib_path"].split("/")
if split_path[-1] == "*":
    MULTIPLE_FILES = True

ONE_COMPILE = config.getboolean("launch", "one_compile")
