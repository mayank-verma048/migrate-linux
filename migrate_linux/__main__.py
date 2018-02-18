import os
import argparse as ap

compatible_list = ['Korora']

def main():
 p = ap.ArgumentParser()
 p.add_argument('destination')
 args=p.parse_args()

 if(os.geteuid()!=0):
  exit('You need to be root to run this script.\nExiting...')

 #Get probes
 import prober

 '''Diagnostic message'''
 probes = prober.get_probe(args.destination)
 print probes
 
 #Call OS specific script
 if probes[0][0] in compatible_list:
  exec('import '+probes[0][0])
  exec(probes[0][0]+'.start(probes,args.destination)')
 else: 
  print 'migrate_linux currently doesn\'t support your distribution. Exiting.'
  exit(1)

 

if __name__=='__main__':
 main()
