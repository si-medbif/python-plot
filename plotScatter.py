#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Harald Grove"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import time
import sys

COLORS= ['#e6194b','#3cb44b','#ffe119','#0082c8','#f58231','#911eb4','#46f0f0','#f032e6','#d2f53c','#fabebe',
        '#008080','#e6beff','#aa6e28','#fffac8','#800000','#aaffc3','#808000','#ffd8b1','#000080','#808080',
         '#FFFFFF','#000000']

def plot_scatter(args):
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    df = pd.read_table(args.infile, sep='\t', header=0)
    y = args.yaxis - 1
    if args.xaxis == 0:
        df.plot(kind='line',y=y, c=COLORS[0], ax=ax)
    else:
        x = args.xaxis-1
        df.plot(kind='scatter', x=x, y=y, c=COLORS[0], edgecolors='none',
                s = 10, ax = ax, zorder = 1)
    ax.set_xlabel('{}'.format(args.xaxis))
    ax.set_ylabel('{}'.format(args.yaxis))
    # *****************************************************
    # Create the Legend, place it in the first frame
    #recs = []
    #for i,n in enumerate(df['groups']):
    #    recs.append(mpatches.Rectangle((0,0),1,1,fc=COLORS[i]))
    #ax.legend(recs,db['highlights'],loc=0,framealpha=0)
    plt.tight_layout()
    outplot = '{}.png'.format(args.infile.rsplit('.',1)[0])
    fig.savefig(outplot)

def plot_lastz1(args):
    """
    Plots the alignment score vs the alignment length
    :param args.infile:
    :return:
    """
    head = ['score','name1','strand1','size1','zstart1','end1',
            'name2','strand2','size2','zstart2','end2',
            'identity','idPct','coverage','covPct']
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    df = pd.read_table(args.infile, sep='\t', header=None,names=head, comment='#')
    df['length'] = df.apply(lambda row: int(row['coverage'].split('/')[0]), axis=1)
    x = 'length'
    y = 'score'
    df.plot(kind='scatter', x=x, y=y, c=COLORS[0], edgecolors='none', s = 10, ax = ax, zorder = 1)
    ax.set_xlabel('{}'.format(x))
    ax.set_ylabel('{}'.format(y))
    # *****************************************************
    # Create the Legend, place it in the first frame
    #recs = []
    #for i,n in enumerate(df['groups']):
    #    recs.append(mpatches.Rectangle((0,0),1,1,fc=COLORS[i]))
    #ax.legend(recs,db['highlights'],loc=0,framealpha=0)
    plt.tight_layout()
    outplot = '{}.png'.format(args.infile.rsplit('.',1)[0])
    fig.savefig(outplot)

def main(args):
    """ Main entry point of the app """
    if args.option == 'scatter':
        plot_scatter(args)
    elif args.option == 'lastz1':
        plot_lastz1(args)
    if args.log:
        with open('README.txt', 'a') as fout:
            fout.write('[{}]\t[{}]\n'.format(time.asctime(), ' '.join(sys.argv)))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("option", help="Type of plot")
    parser.add_argument("infile", help="Input file")

    # Optional argument flag which defaults to False
    parser.add_argument('-l', '--log', action="store_true", default=False, help="Save command to 'README.txt'")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-x", "--xaxis", action="store", type=int, default=1)
    parser.add_argument("-y", "--yaxis", action="store", type=int, default=2)

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
