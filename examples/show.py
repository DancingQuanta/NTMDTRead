import sys, os
import matplotlib.pyplot as plt
from glob import glob
import random


__author__="KOLANICH"
__license__="GPL-3.0+"
__copyright__=r"""Copyright (C) 2004 David Necas (Yeti), Petr Klapetek.
E-mail: yeti@gwyddion.net, klapetek@gwyddion.net.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA."""

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from NTMDTRead.NTMDTReader import NTMDTReader

testDataDir=os.path.join(os.path.dirname(__file__), '..', "test_data")

from NTMDTRead.palettes.Rainbows import Rainbow1
from NTMDTRead.palettes.Stylish import BasicRed
palettes=[Rainbow1, BasicRed]

def processFilesFromTestFolder(globExpr=testDataDir, moveBad=None, saveImages=None):
	"""Shows frames from scans and moves badly parsed ones into a specified folder for investigation"""
	if not globExpr.endswith(".mdt"):
		globExpr=os.path.join(dir, "*.mdt")
	mdts=glob(globExpr)
	for fn in mdts:
		print(fn)
		dir=os.path.dirname(fn)
		bn=os.path.basename(fn)
		try:
			m=NTMDTReader(fn)
			for i, fr in enumerate(m.parsed.frames.frames):
				#try:
				fig, ax = plt.subplots()
				
				if hasattr(m.size[0], "magnitude"):
					w_mag=m.size[0].magnitude
				else:
					w_mag=m.size[0]
				
				if hasattr(m.size[1], "magnitude"):
					h_mag=m.size[1].magnitude
				else:
					h_mag=m.size[1]
				
				ax.imshow(fr.main.frame_data.image, cmap=random.choice(palettes), extent=(0, w_mag, 0, h_mag))
				ax.set_title(
					bn+" : ["+str(i)+"] "+fr.main.frame_data.title.title+"\n"+
					str(m.parsed.frames.frames[0].main.type)
				)
				ax.set_xlabel(m.size[0])
				ax.set_ylabel(m.size[1])
				
				fig.show()
				plt.show(block=True)
		except Exception as ex:
			print("failed:", ex)
			if moveBad:
				badPath=os.path.join(dir, moveBad, bn)
				os.rename(fn, badPath)

if __name__ == "__main__":
	#testOnFiles(moveBad="bad")
	print(__license__)
	processFilesFromTestFolder(testDataDir+"/OK/test_grating*.mdt")