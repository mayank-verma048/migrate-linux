import os
import argparse as ap

def main():
 p = ap.ArgumentParser()
 p.add_argument('destination')
 args=p.parse_args()

 if(os.geteuid()!=0):
  exit('You need to be root to run this script.\nExiting...')

 #Get probes
 import prober

 '''Diagnostic message'''
 print prober.get_probe(args.destination)
 
 #Call OS specific script
 

if __name__=='__main__':
 main()
