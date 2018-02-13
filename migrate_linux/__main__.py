import os

if(os.geteuid()!=0):
 exit('You need to be root to run this script.\nExiting...')

#Get probes
import prober

print prober.probe
