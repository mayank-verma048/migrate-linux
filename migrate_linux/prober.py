from fstab import Line
from fstab import Fstab
import json
import subprocess
import os
import re

#Gets the Partition table type of given physical disk 'disk'
def prb_tbl(disk):

 '''shell=True is a vulnerability'''
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
 return result

#Gets all prerequisite information.
def get_probe(dest):
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

 #Probe Partition Table of source 
 print 'Probing Partition Table'
 
 '''Get boot disk START'''

 '''shell=True is a potential vulnerability. 
    Also the regular expression assumes the input is correct. 
    It only checks for when vgname ends. 
    Invalid vgnames due to the names being reserved are not checked.
 '''
 blkj=json.loads(subprocess.check_output('/bin/lsblk -o name,type,mountpoint -J -s',shell=True)) #lsblk JSON object
 for li in blkj['blockdevices']:
  if(li['mountpoint']=='/boot'):
   st = 'li'
   while(eval(st+'[\'type\']') != 'disk'):
    st+='[\'children\'][0]'
   disk= eval(st+'[\'name\']')
 '''Get boot disk END'''

 res=prb_tbl(disk)
 if(res['Partition Table'] == ''):
  print 'Could not probe partition table type of source.\nExiting.'
  exit(1)
 probe.append(res['Partition Table'])

 #Probe partition table of destination 
 res=prb_tbl(dest) 
 if(res['Partition Table'] == ''):
  print 'Could not probe partition table type of destination.\nExiting.'
  exit(1)
 probe.append(res['Partition Table'])

 #Probe if booted with EFI
 print 'Checking if booted with EFI'
 probe.append(os.path.exists('/sys/firmware/efi'))
 
 #Probe if LVM
 print 'Checking if root is in LV'   
 for li in blkj['blockdevices']:
  if(li['mountpoint']=='/'):
   st = 'li'
   while((eval(st+'[\'type\']') != 'lvm') and (eval(st+'[\'type\']') != 'disk') ):
    st+='[\'children\'][0]'

   '''
    The regular expression assumes the input is correct. 
    It only checks for when vgname ends. 
    Invalid vgnames due to the names being reserved are not checked.
   '''
   if(eval(st+'[\'type\']') == 'lvm'):probe.append([True,re.search('[a-zA-Z0-9+._]([a-zA-Z0-9+._]|--)*',eval(st+'[\'name\']')).group(0)])
   else:probe.append([False,''])

 #Probe fs structure
 print 'Probing filesystem structure'   
 for li in blkj['blockdevices']:
  if(li['mountpoint']=='/'):
   st = 'li'
   tp=str()
   while((eval(st+'[\'type\']') != 'disk') ):
    tp+=eval(st+'[\'type\']')
    tp+='-'
    st+='[\'children\'][0]'
   tp+=eval(st+'[\'type\']')
   probe.append(tp) 


 return probe
