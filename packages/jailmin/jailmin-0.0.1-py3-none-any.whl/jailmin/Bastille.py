# core
import os
import subprocess

def getAllJails():
  RunningJails = getJails()

  BASEPATH = '/usr/local/bastille/jails'
  ret = {}
  for file in os.listdir(BASEPATH):
    # print (file)
    ret[file] = {
      'id': file,
      'path': BASEPATH + '/' + file,
    }
    ret[file]['isRunning'] = file in RunningJails

  return ret

def getJails():
  result = subprocess.run(['bastille','list'], capture_output=True, text=True)
  ret = {}
  for line in str(result.stdout).splitlines():
    words = line.split()
    if words[0] != 'JID':
      JailInfo = {
        'id': words[0]
      }
      offset = 0 if len(words) == 3 else 1      
      JailInfo['hostname'] = words[offset + 1]
      JailInfo['path'] = words[offset + 2]

      ret[JailInfo['id']] = JailInfo

  # print (ret)

  print (result.stderr)
  return ret