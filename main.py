import argparse
import sys

import rgb_to_human_color as ml_color
#===============================================================================================
usage = '''Usage:
	main.py -lr <learning rate> -m <momentum> -e <epochs>
[Options]
	-lr       learning rate 0<lr<1
	-m        momentum 0<m<1
	-e        epochs'''

#===============================================================================================
def print_usage_and_exit(exitMsg : str = ""):
	print(usage)
	sys.exit(exitMsg)

#===============================================================================================
def restricted_float(x): # https://stackoverflow.com/a/12117065
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x
#===============================================================================================
def parse_args():
	parser = argparse.ArgumentParser(description='colorML argParser')
	mutualExclusion = parser.add_mutually_exclusive_group()
	parser.add_argument('-lr', type=restricted_float)
	parser.add_argument('-m', type=restricted_float)
	parser.add_argument('-e', type=int)
	args = parser.parse_args()

	return args

if __name__ == '__main__':

    args = parse_args()
    m = ml_color.Model(args.e, args.lr, args.m)
    m.buildModel()
    m.train()
    m.verify()