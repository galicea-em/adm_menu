#!/usr/bin/python3

import os
import subprocess
import json
import argparse
import getpass

# .ini -> RECIPIENT, STORE
import sys
sys.path.append('../lib')
from ini import Config
cfg = Config("/etc/integration/certs.ini")
RECIPIENT = cfg.config.get('inicerts','RECIPIENT')
STORE_PATH = cfg.config.get('inicerts','STORE_PATH')

PASSPHRASE=None
GPG_BIN = 'gpg2' # w pgp nie ma opcji --output - dlatego pgp2


# This command adds key info to ssh-agent
# see: https://github.com/ulmenhaus/env/blob/33f07be079bc7c1caa8108ffafd726ed06a0bd45/bin/ssh-add-with-password
 
EXPECT_CMDS = """
spawn ssh-add %(key_path)s;
expect "Enter passphrase for %(key_path)s:";
send "%(key_pass)s\r";
expect eof
"""


def agent_store(key_file_name, password):
#    ssh_agent_setup.setup()
    cmds = EXPECT_CMDS % {
        'key_path': key_file_name,
        'key_pass': password,
    }
    try:
#        print(cmds)
        process = subprocess.Popen(["expect"], stdin=subprocess.PIPE,
              stdout=subprocess.PIPE, stderr = subprocess.STDOUT,
              shell=False,
              encoding='utf8')
        stdout, stderr = process.communicate(cmds)
        return process.wait(), stdout
    except subprocess.CalledProcessError:
        print("Exception adding ssh key, shutting down")
        raise Exception
    else:
        print("SSH key loaded")

class CertsPasswordStore(object):

    passwords = []
    def __init__(self, path=None):
        if not path:
          path=os.path.join(os.getenv("HOME"), STORE_PATH)
        if not path:
          path=os.path.join(os.getenv("HOME"), ".password-store") 
        self.storePath= os.path.abspath(path) #os.path.realpath(path)
        if os.path.isfile(self.storePath):
            self.decrypt_passwords()
        else:
            self.encrypt_passwords()

    def add_password(self, ident, password):
      self.passwords.append(
          { 'cert' : ident, 'password': password},
      )
        
    def encrypt_passwords(self):
        gpg = subprocess.Popen(
            [
                GPG_BIN,
                '-e',
                '--recipient', RECIPIENT,
                '--passphrase', PASSPHRASE,
                '--batch',
                '--no-tty',
                '--yes',
                '-vv',
                '-o', self.storePath
            ],
            shell=False,
            stdin=subprocess.PIPE
        )
        gpg.stdin.write(json.dumps(self.passwords).encode())
        gpg.stdin.close()
        gpg.wait()
        if gpg.returncode != 0:
            print(gpg.returncode)
            raise Exception('Couldn\'t encrypt %s' % self.storePath)

    def decrypt_passwords(self):
        gpg = subprocess.Popen(
            [
                GPG_BIN,
                '--quiet',
                '--batch',
                '--passphrase', PASSPHRASE,
                '--pinentry-mode', 'loopback',
                '-d', self.storePath,
            ],
            shell=False,
            stdout=subprocess.PIPE
        )
        gpg.wait()
        if gpg.returncode == 0:
            self.passwords=json.load(gpg.stdout)
        else:
            raise Exception('Couldn\'t decrypt %s' % self.storePath)

usage="Usage: ./inicerts.py -i \nread from .password-store (cert,pass) and send to ssh-agent\nor:  ./inicerts.py -a <ident> -p <password> "
script_name = 'inicerts'
parser = argparse.ArgumentParser(prog = script_name, description = usage)
parser.add_argument('-i', help='Start Agent', action='store_true')
parser.add_argument('-a', help='New item', default='')
parser.add_argument('-p', help='Password', default='')
args = parser.parse_args()


if args.a:
  PASSPHRASE=getpass.getpass("GPG Password : ") 
  store=CertsPasswordStore()
  store.add_password(args.a, args.p)
  store.encrypt_passwords()
elif args.i:
  PASSPHRASE=getpass.getpass("GPG Password : ") 
  store=CertsPasswordStore()
  print('Init...')
  for p in store.passwords:
    fn=os.path.expanduser('~/.ssh/'+p['cert'])
    print(fn)
#    print(p['password'])
    agent_store(fn, p['password'])
else:
  print(usage)