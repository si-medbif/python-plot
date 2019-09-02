#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Harald Grove"
__version__ = "0.1.0"
__license__ = "MIT"

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys

infile = sys.argv[1]
outfile = infile+'.pdf'
pp = PdfPages(outfile)

with open(infile, 'r') as fin:
    line = next(fin)
    if len(line.split()) == 2:
        rdot = True
    else:
        rdot = False

if rdot:
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(7,7))
    with open(infile, 'r') as fin:
        header = None
        x = []
        y = []
        for line in fin:
            if header is None:
                header = line.strip().split()
                continue
            try:
                a,b = line.strip().split()
            except KeyError:
                pass
            if a == 'NA':
                continue
            x.append(int(a))
            y.append(int(b))
            if len(x) == 2:
                axes.plot(x,y, color='black')
                x = []
                y = []
        axes.set_xlabel(header[0])
        axes.set_ylabel(header[1])
        pp.savefig()
    pp.close()
else:
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(7,7))
    with open(infile, 'r') as fin:
        header = None
        x_name = ''
        y_name = ''
        for line in fin:
            if header is None:
                header = line.strip().split()
                continue
            try:
                l = line.strip().split()
            except KeyError:
                pass
            if x_name == '':
                x_name = l[1]
                y_name = l[6]
            if l[1] != x_name or l[6] != y_name:
                axes.set_xlabel(x_name)
                axes.set_ylabel(y_name)
                pp.savefig()
                x_name = l[1]
                y_name = l[6]
            x = int(l[4]),int(l[5])
            y = int(l[9]),int(l[10])
            c = float(l[12].strip('%'))
            if c > 99:
                color = 'black'
                rank = 4
            elif c > 90:
                color = 'green'
                rank = 3
            elif c > 80:
                color = 'orange'
                rank = 2
            else:
                color = 'red'
                rank = 1
            axes.plot(x,y, color=color,zorder=rank)
        axes.set_xlabel(x_name)
        axes.set_ylabel(y_name)
        pp.savefig()
    pp.close()
