import os
import subprocess
import decimal
import socket
import fcntl
import struct
import array
import time
import sys
import platform;
import urllib
import urllib2

try:
  is_64bits = sys.maxsize > 2**32
except AttributeError:
  import platform
  if platform.architecture()[0] == '32bit':
    is_64bits = False

debug=False;


def send(data, core, key, host):
  if debug:
    print("Sending data")
  try:
    import json
  except:
    import simplejson as json

  current_time=time.strftime('%Y-%m-%d %H:%M:%S')
  json_string=json.dumps({"host": core, current_time:data})

  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = urllib2.Request('http://api.hostplot.me/v1/metric', data=json_string)
  request.add_header('X-org-key', key)
  request.add_header('X-host-key', host)
  request.get_method = lambda: 'POST'

  try:
    response = opener.open(request)
    response.read()
    print("Success")
    quit(0)
  except:
    print("Error")
    quit(1)


def cpu_count():
  ''' Returns the number of CPUs in the system '''
  num = 1
  if sys.platform == 'win32':
    # fetch the cpu count for windows systems
    try:
      num = int(os.environ['NUMBER_OF_PROCESSORS'])
    except (ValueError, KeyError):
      pass
  elif sys.platform == 'darwin':
    # fetch teh cpu count for MacOS X systems
    try:
      num = int(os.popen('sysctl -n hw.ncpu').read())
    except ValueError:
      pass

  else:
    # an finally fetch the cpu count for Unix-like systems
    try:
      num = os.sysconf('SC_NPROCESSORS_ONLN')
    except (ValueError, OSError, AttributeError):
      pass

  return num


def get_core_info():
  return {"cpus":cpu_count(), "hostname":platform.node(),"os":platform.system()}

def get_network_bytes(interface):
  f=open('/proc/net/dev', 'r')
  lines=f.read().split("\n")[2:]
  for line in lines:
    if interface in line:
      data=line.split(':')[1].split()
      rx_bytes, tx_bytes=(data[0], data[8])
      return [int(rx_bytes), int(tx_bytes)]



def all_interfaces():
  max_possible = 128  # arbitrary. raise if needed.
  bytes = max_possible * 32
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  names = array.array('B', '\0' * bytes)
  outbytes = struct.unpack('iL', fcntl.ioctl(
      s.fileno(),
      0x8912,  # SIOCGIFCONF
      struct.pack('iL', bytes, names.buffer_info()[0])
  ))[0]
  namestr = names.tostring()
  if is_64bits:
    lst = []
    for i in range(0, outbytes, 40):
      name = namestr[i:i+16].split('\0', 1)[0]
      ip   = namestr[i+20:i+24]
      lst.append([name, format_ip(ip)])
    return lst
  else:
    ret=[]
    vals=[namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]
    for int in vals:
      ret.append([int,'0.0.0.0'])
    return ret


def format_ip(addr):
  return str(ord(addr[0])) + '.' + \
    str(ord(addr[1])) + '.' + \
    str(ord(addr[2])) + '.' + \
    str(ord(addr[3]))


def getload():
  if debug:
    print("Getting load")
  load = os.getloadavg()
  return {'one': round(load[0], 2),
          'five': round(load[1], 2),
          'fifteen': round(load[2], 2)}


def getdisk():
  if debug:
    print("Getting disk information")
  df=subprocess.Popen(["df", "-l", "-P"], stdout=subprocess.PIPE)
  disks=df.communicate()[0].decode().split("\n")[1:-1]
  found_disks={}
  for disk in disks:
    if disk.startswith("/dev"):
      device=disk.split()[0]
      found_disks[str(disk.split()[5])]={'dev':str(disk.split()[0]),
                                    'total':int(disk.split()[1])*1024,
                                    'used':int(disk.split()[2])*1024,
                                    'free':int(disk.split()[3])*1024,
                                    'percent':str(disk.split()[4])}
  return found_disks


def getmemory():
  if debug:
    print("getting memory")
  free=subprocess.Popen(["free", "-b"], stdout=subprocess.PIPE)
  output=free.communicate()[0].decode().split("\n")[1:]
  return {'ptotal': int(output[0].split()[1]),
          'pused': int(output[0].split()[2]),
          'stotal': int(output[2].split()[1]),
          'sused': int(output[2].split()[2]),
          'buffers': int(output[0].split()[5]),
          'cached': int(output[0].split()[6])}


def getnetwork():
  if debug:
    print("getting network")
  timeout=2
  ret = {}
  interfaces=all_interfaces()
  for int in interfaces:
    rx1,tx1=get_network_bytes(int[0])
    time.sleep(timeout)
    rx2,tx2=get_network_bytes(int[0])

    ret[int[0]] = {'addr':int[1],
                   'rx_total':rx2,
                   'tx_total':tx2,
                   'rx_avg':float((rx2-rx1)/timeout),
                   'tx_avg':float((tx2-tx1)/timeout)}

  return ret


def getusers():
  if debug:
    print("Getting users")
  who=subprocess.Popen(["who", "-q"], stdout=subprocess.PIPE)
  output=who.communicate()[0].decode().split("\n")[1:-1]
  return {'count':int(output[0].split('=')[1])}


def getprocesses():
  if debug:
    print("Getting processes")
  ps=subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
  output=ps.communicate()[0].decode().split("\n")[1:]
  return {'count':len(output)}


try:
  import argparse
  parser = argparse.ArgumentParser(description='Collect core metrics and send to the hostplot.me API')
  parser.add_argument("key", help="Your hostplot.me account key.")
  parser.add_argument("host", help="Your hostplot.me host UUID for this host.")
  parser.add_argument("-m", "--metrics", default='all', help="The metrics you wish to run.")
  args = parser.parse_args()
  key=args.key
  host=args.host
except ImportError:
  import optparse
  parser = optparse.OptionParser(usage="usage: %prog [-h] [-m METRICS] key host")
  parser.add_option("-m", "--metrics", default="all", dest="metrics", help="The metrics you wish to run.")
  args, opts = parser.parse_args()
  key=opts[0]
  host=opts[1]


if "all" in args.metrics:
  metrics=['load','disk','memory','network','users','processes']
else:
  metrics=args.metrics.split(',')

data={}
for metric in metrics:
  if debug:
    print("Processing metric", metric)
  if metric=="load":
    data['load']=getload()
  elif metric=="disk":
    data['disk']=getdisk()
  elif metric=="memory":
    data['memory']=getmemory()
  elif metric=="network":
    data['network']=getnetwork()
  elif metric=="users":
    data['users']=getusers()
  elif metric=="processes":
    data['processes']=getprocesses()
  else:
    quit(1)

send(data, get_core_info(), key, host)

