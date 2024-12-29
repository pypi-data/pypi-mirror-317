import os
import subprocess
import shutil

# custom
import jailmin.CmdUtil as CmdUtil

def execCmd(args):
  # print (args)

  jails, RawResponse = CmdUtil.getJails()
  MatchedJailId = CmdUtil.matchJailId(args.JailId)
  if MatchedJailId == None:
    print ('Invalid jail id')
    return

  print (f'CONSOLE to: {MatchedJailId}')

  result = subprocess.run(CmdUtil.elevatePermissions(['bastille','console', MatchedJailId]))
  print (f'returncode: {result.returncode}')
  # if result.returncode == 0:
  #   print (result.stdout.decode('utf-8'))
  # else:
  #   print (result.stderr.decode('utf-8'))

def addParser(parser):
  ConsoleParser = parser.add_parser('console', 
    aliases = ['con'],
    help='overloaded Bastille console command', 
  )
  ConsoleParser.add_argument('JailId')
  ConsoleParser.set_defaults(func=execCmd)
