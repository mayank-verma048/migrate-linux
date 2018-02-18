import tcolor as tc
import subprocess

def chk_drv():
 drv = str()
 try:
  '''shell=True is a potential vulnerability.
  '''
  drv = subprocess.check_output('lsmod | grep nvidia',shell=True)
 except subprocess.CalledProcessError as e :
  if(e.returncode==1):pass
  else:
   tc.printclr(tc.RED,'Unkown error. Exiting.')
   exit(1)

 if('nvidia' in drv):
   tc.printclr(tc.RED,'WARNING: Proprietary Nvidia drivers found!')
   print ' Your X Server might crash on new hardware.'

def start(probes,dest):
 print 'Welcome to Korora migration script'

 if('lvm-part-disk' not in probes[5]):
  print 'Non LVM or LVM on xyz configuration is not supported as of now.'
  exit(0)
 else:
  #Check for drivers that might crash on another system. 
  chk_drv()
   
  #Check if LVM
  if(probes[4][0]==True):
   #Check destination for free space
   print 'Checking destination for free space.'
  
   
  
