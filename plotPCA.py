#!/usr/bin/env python3
"""
Plotting script for making quick visualization of PCA calculatins from Plinks --pca option.
"""

__author__ = "Harald Grove"
__version__ = "0.1.1"
__license__ = "MIT"

import argparse
import pandas as pd
import matplotlib
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

COLORS= ['#e6194b','#3cb44b','#ffe119','#0082c8','#f58231','#911eb4','#46f0f0','#f032e6','#d2f53c','#fabebe',
        '#008080','#e6beff','#aa6e28','#fffac8','#800000','#aaffc3','#808000','#ffd8b1','#000080','#808080',
         '#FFFFFF','#000000']

def plot_pca(args, db):
    eigenvecfile = '{}.eigenvec'.format(args.prefix)
    eigenvalfile = '{}.eigenval'.format(args.prefix)
    df = pd.read_table(eigenvecfile, sep=' ', header=None)
    df1 = pd.read_table(eigenvalfile, sep=' ', header=None)
    for key in db:
        try:
            df[key] = db[key]
        except ValueError:
            continue
    skipped = 0
    pcs = []
    cpcs = []
    palette = {}
    for i in range(len(df1)):
        pcs.append(100 * df1[0][i] / sum(df1[0]))
        cpcs.append('{:.1f}'.format(sum(pcs)))
    fig, ax = plt.subplots(2,2,figsize=(10,10))
    # *****************************************************
    # Plot Scree plot, lower left
    x = np.arange(1,len(pcs)+1)
    ax[1,0].plot(x,pcs)
    for i, txt in enumerate(cpcs):
        #print(i, txt, x[i], pcs[i])
        ax[1,0].annotate(cpcs[i], (x[i],pcs[i]))
    ax[1,0].set_ylabel('Explained variance pr. PC [%]')
    ax[1,0].set_xlabel('Principal Component (PC)')
    ax[1,0].set_xlim([0,len(pcs)+1])
    ax[1,0].set_xticks(x)
    # *****************************************************
    # Plot PC1&PC2 and PC3&PC4, upper left and right
    df1 = df[df['zorder']==1]
    df2 = df[df['zorder']==2]
    if df1.shape[0] > 0:
        df1.plot(kind='scatter', x=2, y=3, c=df1['colors'], edgecolors='none',
                 s=df1['sizes'], ax=ax[0,0], zorder=1)
        df1.plot(kind='scatter', x=4, y=5, c=df1['colors'], edgecolors='none',
                 s=df1['sizes'], ax=ax[0,1], zorder=1)
    if df2.shape[0] > 0:
        df2.plot(kind='scatter', x=2, y=3, c=df2['colors'], edgecolors='none',
                 s=df2['sizes'], ax=ax[0,0], zorder=2)
        df2.plot(kind='scatter', x=4, y=5, c=df2['colors'], edgecolors='none',
                 s=df2['sizes'], ax=ax[0,1], zorder=2)
    ax[0,0].set_xlabel('PC1 [{}%]'.format(int(pcs[0])))
    ax[0,0].set_ylabel('PC2 [{}%]'.format(int(pcs[1])))
    ax[0,1].set_xlabel('PC3 [{}%]'.format(int(pcs[2])))
    ax[0,1].set_ylabel('PC4 [{}%]'.format(int(pcs[3])))
    # *****************************************************
    # Plot loading plot PC1&PC2, lower right

    # *****************************************************
    # Create the Legend, place it in the first frame
    recs = []
    for i,n in enumerate(db['highlights']):
        recs.append(mpatches.Rectangle((0,0),1,1,fc=COLORS[i]))
    ax[0,0].legend(recs,db['highlights'],loc=0,framealpha=0)
    plt.tight_layout()
    outplot = '{}.png'.format(args.prefix)
    fig.savefig(outplot)

def read_samples(args, db):
    """
    Reads and sets information for each sample in the plot
    """
    with open(args.samples, 'r') as fin:
        for line in fin:
            sample, group = line.strip().split(None, 2)[0:2]
            if group in db['highlights']:
                db['groups'].append(group)
                db['sizes'].append(50)
                db['markers'].append('.')
                db['zorder'].append(2)
                rank = db['highlights'].index(group)
                db['colors'].append(COLORS[rank])
            else:
                db['groups'].append(group)
                db['sizes'].append(5)
                db['markers'].append('.')
                db['zorder'].append(1)
                db['colors'].append('#dddddd')

def read_family(args, db):
    """
    Reads and sets information for each sample in the plot
    """
    with open(args.family, 'r') as fin:
        for line in fin:
            fid, iid, father, mother, sex, pheno = line.strip().split(None, 6)[0:6]
            group = [fid, iid, father, mother, sex, pheno][args.column-1]
            if pheno in db['highlights']:
                db['groups'].append(group)
                db['sizes'].append(50)
                db['markers'].append('.')
                db['zorder'].append(2)
                rank = db['highlights'].index(group)
                db['colors'].append(COLORS[rank])
            else:
                db['groups'].append(pheno)
                db['sizes'].append(5)
                db['markers'].append('.')
                db['zorder'].append(1)
                db['colors'].append('#dddddd')

def read_default(args, db):
    """
    Reads and sets information for each sample in the plot
    """
    with open('{}.eigenvec'.format(args.prefix), 'r') as fin:
        for line in fin:
            group, sample = line.strip().split(None, 2)[0:2]
            if group in db['highlights']:
                db['groups'].append(group)
                db['sizes'].append(50)
                db['markers'].append('.')
                db['zorder'].append(2)
                rank = db['highlights'].index(group)
                db['colors'].append(COLORS[rank])
            else:
                db['groups'].append(group)
                db['sizes'].append(5)
                db['markers'].append('.')
                db['zorder'].append(1)
                db['colors'].append(COLORS[-1])

def mark_highlights(args, db):
    """
    Change display settings for highlighted groups.
    """
    with open(args.mark, 'r') as fin:
        for line in fin:
            name = line.strip()
            db['highlights'].append(name)

def main(args):
    """ Main entry point of the app """
    db = {'groups':[], 'names':[],'colors':[], 'sizes':[],
          'zorder':[], 'markers':[], 'highlights':[]}
    if args.mark is not None:
        mark_highlights(args, db)
    if args.family is not None and args.samples is not None:
        raise Exception("Options '--family' and '--samples' cannot be used together!")
    if args.samples is not None:
        read_samples(args, db)
    elif args.family is not None:
        read_family(args, db)
    else:
        read_default(args, db)
    plot_pca(args, db)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("prefix", help="File prefix (prefix.eigenvec & prefix.eigenval)")

    # Optional argument flag which defaults to False
    #parser.add_argument('-', '--flag', action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-f", "--family", help="Plink sample information, 6 columns.")
    parser.add_argument("-c", "--column", type=int, help="Column in family file for grouping (1-6).", default=6)
    parser.add_argument("-s", "--samples", help="List of samples (2 columns: sample group).")
    parser.add_argument("-m", "--mark", help="Groups to highlight.")

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
