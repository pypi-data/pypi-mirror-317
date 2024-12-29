# core
import argparse
import subprocess
import importlib.metadata

# custom
import jailmin.CmdConsole as CmdConsole
import jailmin.CmdList as CmdList
import jailmin.CmdUtil as CmdUtil

def cmdPassThrough(args):
  print ('blind pass through')
  print (f'cmd: {args.cmd}')
  JailId = CmdUtil.matchJailId(args.JailId)
  print (f'JailId: {JailId}')
  print (f'args: {args.args}')
  result = subprocess.run(CmdUtil.elevatePermissions(['bastille', args.cmd, JailId] + args.args))
  pass

def addBlindSubparser(parser, cmd):
  subparser = parser.add_parser(cmd, 
    # aliases = ['con'],
    # help='overloaded Bastille console command', 
  )
  subparser.add_argument('JailId')
  subparser.add_argument('args', nargs=argparse.REMAINDER)
  subparser.set_defaults(func=cmdPassThrough)

def doCli():
  # print (__name__)
  print(f"Jailmin version {importlib.metadata.version('jailmin')}")

  parser = argparse.ArgumentParser(
    prog='jailmin',
    # help='Bastille wrapper'
  )
  cmdparser = parser.add_subparsers(dest='cmd')

  CmdConsole.addParser(cmdparser)
  CmdList.addParser(cmdparser)
  addBlindSubparser(cmdparser, 'stop')
  addBlindSubparser(cmdparser, 'start')
  addBlindSubparser(cmdparser, 'restart')

  parser.set_defaults(func=cmdPassThrough)

  args = parser.parse_args()
  # print (f"cmd: {args.cmd}")
  if args.cmd:
    args.func(args = args)
  else:
    CmdList.execCmd(args = args)

