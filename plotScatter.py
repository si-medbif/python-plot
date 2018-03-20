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

class plotScatter(object):

    def __init__(self, input, bins=None, column="1,2"):
        self.colors = ['#e6194b','#3cb44b','#ffe119','#0082c8','#f58231','#911eb4','#46f0f0','#f032e6','#d2f53c',
                       '#fabebe','#008080','#e6beff','#aa6e28','#fffac8','#800000','#aaffc3','#808000','#ffd8b1',
                       '#000080','#808080','#FFFFFF','#000000']
        self.inputfile = input
        self.db = {'groups':[], 'colors':[], 'sizes':[], 'zorder':[], 'markers':[]}
        self.binfile = bins
        self.bins = []
        self.groups = []
        self.x, self.y, self.c = [int(cx) for cx in column.split(',')]
        self.outfile = '{}.png'.format(input.rsplit('.',1)[0])

    def plot_scatter(self):
        df = pd.read_table(self.inputfile, header=None, comment='#')
        for key in self.db:
            try:
                df[key] = self.db[key]
            except ValueError:
                print('Invalid column: {}'.format(key))
                continue
        fig, ax = plt.subplots(1,1,figsize=(10,10))
        # *****************************************************
        # Plot scatter plot
        x = self.x - 1
        y = self.y - 1
        df1 = df[df['zorder']==1]
        if df1.shape[0] > 0:
            try:
                df1.plot(kind='scatter', x=x, y=y, c=df1['colors'], edgecolors='none', s=df1['sizes'],ax=ax, zorder=1)
            except KeyError as err:
                print('Blech: {}'.format(err))
                sys.exit(1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        # *****************************************************
        # Create the Legend, place it in the fourth frame
        if len(self.groups) > 0:
            recs = []
            for i,n in enumerate(self.groups):
                recs.append(mpatches.Rectangle((0,0),1,1,fc=self.colors[i]))
            ax.legend(recs,self.groups,loc=0,framealpha=1)
            #ax.text(0.1,0.9,': {}'.format(self.c))
        plt.tight_layout()
        fig.savefig(self.outfile)
        plt.show()

    def read_bins(self):
        """
        Reads binning information, min\tmax\tgroup_name, where: min <= x < max
        """
        with open(self.binfile, 'r') as fin:
            for line in fin:
                try:
                    minval, maxval, group = line.strip().split(None, 3)[0:3]
                except ValueError:
                    continue
                self.bins.append([float(minval),float(maxval),group])

    def read_default(self):
        """
        Reads and sets information for each sample in the plot
        """
        self.groups = []
        if self.c == 0:
            return
        with open(self.inputfile, 'r') as fin:
            for line in fin:
                if line.startswith('#'):
                    continue
                l = line.strip().split()
                value = l[self.c-1].strip('%')
                if len(self.bins) > 0:
                    for minv,maxv,group in self.bins:
                        if float(value) >= minv and float(value) < maxv:
                            break
                    else:
                        group = 'NA'
                    if group not in self.groups:
                        self.groups.append(group)
                    self.db['groups'].append(group)
                    self.db['sizes'].append(30)
                    self.db['markers'].append('.')
                    self.db['zorder'].append(1)
                    rank = self.groups.index(group)
                    self.db['colors'].append(self.colors[rank])
                else:
                    if value not in self.groups:
                        self.groups.append(value)
                    self.db['groups'].append(value)
                    self.db['sizes'].append(30)
                    self.db['markers'].append('.')
                    self.db['zorder'].append(1)
                    rank = self.groups.index(value)
                    self.db['colors'].append(self.colors[rank])

def main(args):
    """ Main entry point of the app """
    sca = plotScatter(args.input,args.bins,args.columns)
    if args.bins is not None:
        sca.read_bins()
    sca.read_default()
    sca.plot_scatter()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("input", help="Tab separated data file")

    # Optional argument flag which defaults to False
    #parser.add_argument('-', '--flag', action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-c", "--columns", help="Columns for x,y,group.", default="1,2,0")
    parser.add_argument("-b", "--bins", help="Values of group column to be treated as one group")
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
