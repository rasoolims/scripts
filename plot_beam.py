#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')

with open(sys.argv[1]) as f:
    data = f.read()

data = data.split('\n')

for row in data:
	print row

x = [row.split('\t')[0] for row in data]
beam1 = [row.split('\t')[1] for row in data]
beam2 = [row.split('\t')[2] for row in data]
beam4 = [row.split('\t')[3] for row in data]
beam8 = [row.split('\t')[4] for row in data]
beam16 = [row.split('\t')[5] for row in data]
beam32 = [row.split('\t')[6] for row in data]
beam64 = [row.split('\t')[7] for row in data]

fig = plt.figure()


ax1 = fig.add_subplot(111)

#ax1.set_title("Plot title...")    
ax1.set_xlabel('Iteration#')
ax1.set_ylabel('Unlabeled accuracy')

ax1.plot(x,beam1,  marker='*', c='green', label='Beam:1')
ax1.plot(x,beam2,  marker='+', c='blue', label='Beam:2')
ax1.plot(x,beam4, marker='<', c='orange', label='Beam:4')
ax1.plot(x,beam8,  marker='1', c='black', label='Beam:8')
ax1.plot(x,beam16,  marker='4',c='purple', label='Beam:16')
ax1.plot(x,beam32,  marker='p', c='brown', label='Beam:32')
ax1.plot(x,beam64, marker='D', c='r', label='Beam:64')

ax1.legend(loc='lower right', shadow=True, prop = fontP)
pp = PdfPages(sys.argv[1]+'.pdf')
pp.savefig(fig)
pp.close()

plt.show()