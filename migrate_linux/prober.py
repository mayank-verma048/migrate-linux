from fstab import Line
from fstab import Fstab

probe = list()

#Probe OS
import platform

print 'Probing OS info'

osinfo=platform.linux_distribution()
if(osinfo[0] == ''):
 print 'Could not probe OS name.\nExiting.'
 exit(1)
elif(osinfo[1] == '' or osinfo[2] == ''):
 print 'Could not probe complete OS information.'
probe.append(platform.linux_distribution())

#Probe Partition Table (Currently won't work for multiple disks)
print 'Probing Partition Table'

'''Get boot disk START'''
import json
import subprocess

blkj=json.loads(subprocess.check_output('/bin/lsblk -o name,type,mountpoint -J -s',shell=True)) #lsblk JSON object
for li in blkj['blockdevices']:
 if(li['mountpoint']=='/boot'):
  st = 'li[\'children\'][0]'
  while(eval(st+'[\'type\']') != 'disk'):
   st+='[\'children\'][0]'
  disk= eval(st+'[\'name\']')
'''Get boot disk END'''

output = subprocess.check_output("parted -l", shell=True)
result = {}
i=-1
for row in output.split('\n'):
 if(i>-1 and i<1):
  i+=1
  continue
 if(i==1):
  '''Required row found'''
  key, value = row.split(': ') 
  result[key.strip(' .')] = value.strip()
  break
 if '/dev/'+disk in row:
  i=0
  continue
 else: continue

if(result['Partition Table'] == ''):
 print 'Could not probe partition table type.\nExiting.'
 exit(1)
probe.append(result['Partition Table'])

