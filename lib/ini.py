#!/usr/bin/python

import sys, os
import configparser
from pprint import pprint

class Config():

    config_path = None
    config = None

    def __init__(self, config_path=None, debug=False):
      self.debug=debug
      self.config_path=config_path
      if self.config_path:
        self.config=self.read_config(config_path)

    def read_config(self, file_name):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(file_name, encoding="UTF-8")
        except KeyError as e:
            self.shutdown_with_error(
                "Configuration file is invalid! (Key not found: " + str(e) + ")")
        if self.debug:
          self.dump()
        return self.config

    def dump(self):
      if not self.config:
        print('Empty!')
      else:
        for sec in self.config.sections():
          pprint(sec)
          for par in self.config[sec]:
            pprint('%s = %s' % (par,self.config[sec][par]))


if __name__ == '__main__':
  cfg = Config("/etc/integration/certs.ini", True)
