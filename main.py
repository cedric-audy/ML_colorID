import argparse
import sys
import tkinter as tk
from csv import writer
import teach_me_colors as trainer
import rgb_to_human_color as ml_color

# ===============================================================================================
TRAINING_DATA = './data/color_training.csv'
# ===============================================================================================
VERIF_DATA = './data/color_verif.csv'
#===============================================================================================
ACCURACY_DATA = './data/accuracy.csv'
#===============================================================================================
usage = '''Usage:
	main.py -lr <learning rate> -m <momentum> -e <epochs>
[Options]
	-lr       learning rate 0<lr<1
	-m        momentum 0<m<1
	-e        epochs

    -vr input verification data
    -tr input training data
    '''
#===============================================================================================
def print_usage_and_exit(exitMsg : str = ""):
	print(usage)
	sys.exit(exitMsg)
#===============================================================================================
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
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
	parser.add_argument('-lr', type=restricted_float)
	parser.add_argument('-m', type=restricted_float)
	parser.add_argument('-e', type=int)
	mutualExclusion = parser.add_mutually_exclusive_group()
	mutualExclusion.add_argument('--load', type=str)
	mutualExclusion.add_argument('-tr', action='store_true')
	mutualExclusion.add_argument('-vr', action='store_true')
	mutualExclusion.add_argument('-p', action='store_true')
	args = parser.parse_args()

	return args
#===============================================================================================
def run(e, lr, mom, ask=True):
    m = ml_color.Model(TRAINING_DATA, VERIF_DATA, e, lr, mom)
    m.buildModel()
    m.train()
    r = m.verify()
    m.save(ask=ask)
    print(f'{"{:.2}".format(r)},{lr},{mom}')
    append_list_as_row(ACCURACY_DATA,[r,lr,mom])
#===============================================================================================
if __name__ == '__main__':
    import random

    args = parse_args()
    if args.lr == 0:
        while True:
            lr = random.uniform(0.5,1)
            m = random.uniform(0.5,1) if args.m == 0 else args.m
            run(args.e,lr,m)
    elif args.tr or args.vr:
        path = TRAINING_DATA if args.tr else VERIF_DATA
        root = tk.Tk()
        app = trainer.Application(path, master=root)
        app.mainloop()
    elif args.p:
        import plot_test as pl
        data = pl.plotAccuracy(ACCURACY_DATA)
    elif args.load:
        m = ml_color.Model(TRAINING_DATA, VERIF_DATA)
        m.load_model(f'{args.load}')

    else:
        run(args.e,args.lr,args.m)
#===============================================================================================

    