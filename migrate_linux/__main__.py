import os
import argparse as ap

p = ap.ArgumentParser()
p.add_argument('destination')
args=p.parse_args()

if(os.geteuid()!=0):
 exit('You need to be root to run this script.\nExiting...')

#Get probes
import prober

print prober.get_probe(args.destination)
