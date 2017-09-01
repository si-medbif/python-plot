#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Harald Grove"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COLORS = ['blue','green','red','cyan','magenta','yellow','black']

def plot_pca(args, db):
    eigenvecfile = '{}.eigenvec'.format(args.prefix)
    eigenvalfile = '{}.eigenval'.format(args.prefix)
    df = pd.read_table(eigenvecfile, sep=' ', header=None)
    df1 = pd.read_table(eigenvalfile, sep=' ', header=None)
    pcs = []
    pheno = {}
    plotted = []
    for i in range(len(df1)):
        pcs.append(100 * df1[0][i] / sum(df1[0]))
    fig, ax = plt.subplots(2,2,figsize=(10,10))
    for index,row in df.iterrows():
        if row[0] in db:
            size = db[row[0]]['size']
            color = db[row[0]]['color']
            zorder = db[row[0]]['zorder']
            marker = db[row[0]]['marker']
            group = db[row[0]]['group']
        else:
            continue
        if color != 'gray':
            if group not in plotted:
                plotted.append(group)
            pheno[group] = color
        else:
            if 'Misc.' not in plotted:
                plotted.append('Misc.')
            pheno['Misc.'] = color
        ax[0,0].scatter(row[2],row[3],\
                        s=size,c=color,\
                        edgecolors='none',\
                        marker=marker, zorder=zorder)
        #ax[0,0].text(row[2]+0.01,row[3]+0.01,row[0])
        ax[0,1].scatter(row[4],row[5],\
                        s=size,c=color,\
                        edgecolors='none',\
                        marker=marker, zorder=zorder)
        #ax[0,1].text(row[2]+0.01,row[3]+0.01,row[0])
    ax[0,0].set_xlabel('PC1 [{}%]'.format(int(pcs[0])))
    ax[0,0].set_ylabel('PC2 [{}%]'.format(int(pcs[1])))
    ax[0,1].set_xlabel('PC3 [{}%]'.format(int(pcs[2])))
    ax[0,1].set_ylabel('PC4 [{}%]'.format(int(pcs[3])))
    #***********************
    recs = []
    for i in plotted:
        recs.append(mpatches.Rectangle((0,0),1,1,fc=pheno[i]))
        ax[1,0].legend(recs,plotted,loc=0,framealpha=0)
    plt.tight_layout()
    outplot = '{}.png'.format(args.prefix)
    fig.savefig(outplot)

def read_label(args, db):
    with open(args.label, 'r') as fin:
        for line in fin:
            sample, group = line.strip().split()
            db[sample] = {'group':group,'size':50,\
                          'marker':'.','zorder':1,\
                          'color':'gray'}
            if group not in db['groups']:
                db['groups'][group] = []
            db['groups'][group].append(sample)

def mark_highlights(args, db):
    with open(args.mark, 'r') as fin:
        c_ind = 0
        for line in fin:
            name = line.strip()
            for sample in db['groups'][name]:
                db[sample]['size'] = 100
                db[sample]['color'] = COLORS[c_ind]
                db[sample]['zorder'] = 5
                db[sample]['marker'] = 'o'
            c_ind += 1

def main(args):
    """ Main entry point of the app """
    db = {'groups':{}}
    if args.label is not None:
        read_label(args, db)
    if args.mark is not None:
        mark_highlights(args, db)
    plot_pca(args, db)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("prefix", help="File prefix (.eigenvec & .eigenval)")

    # Optional argument flag which defaults to False
    parser.add_argument('-f', '--flag', action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-l", "--label", action="store")
    parser.add_argument("-m", "--mark", help="Samples to highlight.")

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
