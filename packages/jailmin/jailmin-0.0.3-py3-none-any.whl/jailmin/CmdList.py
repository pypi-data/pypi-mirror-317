import json
import os
import re
import subprocess
import shutil

# custom
import jailmin.CmdUtil as CmdUtil


def execCmd(args):
  # print (args)

  jails, RawResponse = CmdUtil.getJails()

  if not jails is None:
    if 'json' in args and args.json:
      print (json.dumps(jails, indent=2))
    else:
      print (RawResponse)

  return jails

def addParser(cmdparser):
  ListParser = cmdparser.add_parser('list', 
    aliases=['ls'],
    help='overloaded Bastille list command', 
  )
  ListParser.add_argument('-j', '--json', default = False, action='store_true')
  ListParser.set_defaults(func=execCmd)
