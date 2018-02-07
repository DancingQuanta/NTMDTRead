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

from vispy import app, scene
import scipy as np

def plot3d(m, bn):
	for i, fr in enumerate(m.parsed.frames.frames):
		#fr.main.frame_data.image, cmap=random.choice(palettes), extent=(0, w_mag, 0, h_mag)
		xs=np.linspace(0, 1, fr.main.frame_data.image.shape[0])
		ys=np.linspace(0, 1, fr.main.frame_data.image.shape[1])
		
		canvas = scene.SceneCanvas(keys='interactive', title=bn)
		view = canvas.central_widget.add_view()
		view.camera = scene.TurntableCamera(up='z')

		# Simple surface plot example
		# x, y values are not specified, so assumed to be 0:50
		p1 = scene.visuals.SurfacePlot(
			x=xs,y=ys,
			z=fr.main.frame_data.image
			#,shading='smooth'
		)
		#p1.attach(scene.filters.ZColormapFilter(random.choice(palettes)))
		#p1.attach(scene.filters.ZColormapFilter("fire"))
		view.add(p1)

		# Add a 3D axis to keep us oriented
		axis = scene.visuals.XYZAxis(parent=view.scene)
		canvas.show()
		app.run()

def plot2d(m, bn):
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
			plot3d(m, bn)
			
		except Exception as ex:
			print("failed:", ex)
			if moveBad:
				badPath=os.path.join(dir, moveBad, bn)
				os.rename(fn, badPath)

if __name__ == "__main__":
	#testOnFiles(moveBad="bad")
	print(__license__)
	processFilesFromTestFolder(testDataDir+"/OK/test_grating*.mdt")