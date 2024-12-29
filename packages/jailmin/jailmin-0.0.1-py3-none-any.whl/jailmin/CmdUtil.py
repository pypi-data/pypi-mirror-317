# core
import os
import subprocess
import re
# custom
import jailmin.Bastille as Bastille

KEY_JAIL_ID = 'JID'

def elevatePermissions(cmds):
  cmds.insert(0,'sudo')
  return cmds

def guessJail(JailPart):
  jails = Bastille.getAllJails()

  ret = []
  for JailId in jails:
    if JailPart in JailId.lower():
      ret.append(JailId)

  if len(ret) == 0:
    return None
  elif len(ret) == 1:
    return ret[0]
  else:
    return ret

def setRcConf(key, value):
  ExitCode = os.system(f'sysrc {key}="{value}"')
  if ExitCode != 0:
    raise Exception(f'Unexpected exit code: {ExitCode}')
  # print (ExitCode)

def readRcConf():
  ret = {}

  RcConf = open('/etc/rc.conf','r')
  for line in RcConf.readlines():
    if line.startswith('bastille_'):
      matches = re.match('bastille_(?P<key>.+?)\s*=\s*"(?P<value>.+)"',line)
      if matches.group('key') == 'list':
        ret[matches.group('key')] = matches.group('value').split(' ')
      else:
        ret[matches.group('key')] = matches.group('value')

  RcConf.close()

  return ret

def matchJailId(TestJailId):
  jails, RawResponse = getJails()

  # exact match iteration
  for jail in jails:
    if TestJailId == jail[KEY_JAIL_ID]: 
      return TestJailId

  # best match iteration
  PossibleJailId = None
  for jail in jails:
    # exact match
    if jail[KEY_JAIL_ID].startswith(TestJailId): 
      # check if there's another possibility
      if PossibleJailId != None:
        # more than one possibility: return None
        raise Exception(f'Multiple matches: {TestJailId}')
      PossibleJailId = jail[KEY_JAIL_ID]

  return PossibleJailId

def getJails():
  result = subprocess.run(
    elevatePermissions(['bastille','list','-a']),
    capture_output = True)

  if result.returncode == 0:
    FieldNames = []
    jails = []
    stdout = result.stdout.decode('utf-8')
    for idx, line in enumerate(stdout.splitlines()):
      if idx == 0:
        for FieldName in re.split(r'\s+', line):
          # print (f'field: {FieldName}')
          FieldNames.append(FieldName)
      else:
        # print (f'New line')
        rec = {}
        for idx, FieldValue in enumerate(re.split(r'\s+', line)):
          FieldName = FieldNames[idx]
          if FieldNames[idx] != '':
            rec[FieldNames[idx]] = FieldValue 
            # print (f'field: {FieldValue}')
        jails.append(rec)
      
    return jails, stdout
  else:
    print (f'ERROR: {result.stderr}')
    return None

# def getJails():
#   IDX_JID = 0
#   IDX_STATE = 1
#   IDX_IP = 2
#   IDX_ADDRESS = 3
#   IDX_HOSTNAME = 4
#   IDX_RELEASE = 5
#   IDX_PATH = 6

#   result = subprocess.run(elevatePermissions(None,['bastille','list','-a']) , capture_output=True, text=True)
#   ret = {}
#   for line in str(result.stdout).splitlines():
#     words = line.split()
#     # print (f"{words}")
#     if words[IDX_JID] != 'JID':
#       JailInfo = {
#         'id': words[IDX_JID]
#       }
#       JailInfo['hostname'] = words[IDX_HOSTNAME]
#       JailInfo['path'] = words[IDX_PATH]
#       JailInfo['state'] = words[IDX_STATE]

#       ret[JailInfo['id']] = JailInfo

#     # print (ret)

#   print (result.stderr)
#   return ret