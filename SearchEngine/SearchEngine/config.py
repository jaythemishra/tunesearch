#!/usr/bin/python
from configparser import ConfigParser

# NOTE: This file isn't being used yet because i couldn't figure
# out how to get the pathnames working w/ the filename stuff.
# gonna try this again when refactoring to clean up connection handling code
#
# i really don't know how python works lol


#
# @function config --   handles configuration for db connection 
# 
# @param filename  --   config file
# @param section   --   section in config file to read from
#
def config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db