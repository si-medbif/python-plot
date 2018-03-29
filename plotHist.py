#!/usr/bin/env python3
"""
Plotting script for making quick histograms.
"""

__author__ = "Harald Grove"
__version__ = "0.1.0"
__license__ = "MIT"

import matplotlib
matplotlib.use('Agg')
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sys

if int(matplotlib.__version__[0]) < 2:
    sys.stderr.write('WARNING: This script was optimized with Matplotlib 2.0.2.\n')
    sys.stderr.write('\tCurrent version of Matplotlib is {}.\n'.format(matplotlib.__version__))
    OLD_VERSION = True
else:
    OLD_VERSION = False

COLORS = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99',
          '#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']

def plot_hist(args, db):
    ds = pd.Series(db['data'])
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    ds.hist(grid=None, ax=ax, bins=args.bins)
    if args.xlim is not None:
        xmin, xmax = args.xlim.split(',')
        plt.xlim(int(xmin), int(xmax))
    plt.tight_layout()
    outplot = '{}.png'.format(args.datafile.rsplit('.',1)[0])
    fig.savefig(outplot)

def plot_cat(args, db):
    df = pd.DataFrame(list(db['catdata'].items()), columns=['key','value'])
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #df['colour'].value_counts().plot(kind='bar')
    df.plot(kind='bar', x='key', y='value', ax=ax)
    outplot = '{}_category.png'.format(args.datafile.rsplit('.', 1)[0])
    fig.savefig(outplot)

def read_samples(args, db):
    """
    Reads and sets information for each sample in the plot
    """
    with open(args.datafile, 'r') as fin:
        for line in fin:
            if line.startswith('#'):
                continue
            line_l = line.strip().split()
            try:
                value = float(line_l[args.column-1])
            except ValueError:
                value = line_l[args.column - 1]
                db['catdata'][value] = db['catdata'].get(value, 0) + 1
                continue
            db['data'].append(value)
            if db['max'] is None:
                db['max'], db['min'] = value, value
                continue
            db['max'] = max(db['max'], value)
            db['min'] = min(db['min'], value)

def main(args):
    """ Main entry point of the app """
    db = {'data':[], 'catdata':{}, 'max':None, 'min':None}
    read_samples(args, db)
    if len(db['data']) > len(db['catdata']):
        plot_hist(args, db)
    else:
        plot_cat(args, db)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("datafile", help="Tab separated data file")

    # Optional argument flag which defaults to False
    parser.add_argument('-k', '--header', action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-c", "--column", type=int, help="Column with data to plot.")
    parser.add_argument("-b", "--bins", type=int, help="Number of bins.")
    parser.add_argument("-x", "--xlim", help="X limits [min,max]")
    #parser.add_argument("-m", "--mark", help="Groups to highlight.")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of '--version'
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s (version {version})'.format(version=__version__))

    args = parser.parse_args()
    main(args)
