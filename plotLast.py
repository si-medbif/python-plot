#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Harald Grove"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import time
import sys
import pandas as pd
import matplotlib.colorbar as colorbar
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.patches as patches
import numpy as np
sns.set_style('white')

def plot_alignment(query, df, suffix=None):
    """ df is a data frame consisting of Last alignments
        suffix is
    """
    print(query)
    db = {}
    maxid, minid = 0,100
    for (index,row) in df.iterrows():
        if row['name2'] != query:
            continue
        minid = min(minid, row['idpct'])
        maxid = max(maxid, row['idpct'])
        q_length = row['seqSize2']
        if row['name1'] not in db:
            db[row['name1']] = len(db) + 1
    y_scale = 10 * len(db)
    y_size = max(10, len(db)//10 * 2)
    fig,axes = plt.subplots(1,3,figsize=(20,y_size), gridspec_kw = {'width_ratios':[16,1,4]})
    axes[0].set_xlim([0,100])
    axes[0].set_ylim([0, y_scale+10])
    axes[1].set_xlim([0,1])
    axes[1].set_ylim([70, 100])
    axes[2].set_xlim([0,20])
    axes[2].set_ylim([0, y_scale+10])
    major_ticks = np.arange(0, y_scale+11, 10)
    axes[0].set_yticks(major_ticks)
    axes[0].set_title('Alignments against {}'.format(query))
    axes[0].set_xlabel('Total length={}'.format(q_length))
    axes[0].grid()
    axes[2].set_yticks(major_ticks)
    axes[2].tick_params(axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom=False,      # ticks along the bottom edge are off
                        top=False,         # ticks along the top edge are off
                        labelbottom=False) # labels along the bottom edge are off
    norm = colors.Normalize(minid, maxid)
    cmap = cm.cool
    for (index,row) in df.iterrows():
        if row['name2'] != query:
            continue
        strand2 = row['strand2']
        adj = row['seqSize2'] // 100
        cov1 = row['alnSize1'] / row['seqSize1']
        x1 = row['start2+'] // adj
        x2 = row['end2+'] // adj
        rank = db[row['name1']]
        color = cmap(norm(row['idpct']))
        if cov1 < 0.5:
            line_w = 4
        else:
            line_w = 0.1
        if strand2 == '+':
            axes[0].add_patch(patches.Rectangle((x1,rank*10),x2-x1,8,facecolor=color,edgecolor='black', linewidth=line_w))
        else:
            axes[0].add_patch(patches.Rectangle((x1,rank*10),x2-x1,8,facecolor=color, edgecolor='black', linewidth=line_w, hatch='/'))
        axes[2].text(0,rank*10+1,row['name1'])
    cb1 = colorbar.ColorbarBase(axes[1], cmap=cmap,norm=norm, orientation='vertical')
    if suffix is not None:
        figurefile = '{}.{}.png'.format(query,suffix)
    else:
        figurefile = '{}.png'.format(query)
    fig.savefig(figurefile, dpi=90, bbox_inches='tight')
    plt.close(fig)

def main(args):
    """ Main entry point of the app """

    df = pd.read_table(args.infile, header=0)
    df.sort_values(['name2', 'start2+'], inplace=True)
    # Make a list of queries to plot, depending on user choice
    queries = []
    if args.query is not None:
        try:
            if args.query in df['name2'].values:
                queries.append(args.query)
            else:
                with open(args.query, 'r') as fin:
                    for line in fin:
                        queries.append(line.strip())
        except FileNotFoundError:
            sys.stderr.write('{} is neither a file nor a valid sequence name, aborting.\n'.format(args.query))
            sys.exit(1)
    else:
        queries = list(df['name2'].unique())
    for query in queries:
        df1 = df[df['name2'] == query]
        plot_alignment(query, df1, args.name)

    if args.log:
        with open('README.txt', 'a') as fout:
            fout.write('[{}]\t[{}]\n'.format(time.asctime(), ' '.join(sys.argv)))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("infile", help="Input file")

    # Optional argument flag which defaults to False
    parser.add_argument('-l', '--log', action="store_true", default=False, help="Save command to 'README.txt'")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", help="Tag to add to the image file")
    parser.add_argument("-q", "--query", action="store", help="List of queries to plot (one pr. image)")

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
