import sys, os
import functools
import lazy_object_proxy
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from .nt_mdt_pal import *
from .kaitaiParseBase import kaitaiParseBase

__author__="KOLANICH"
__license__="Unlicense"
__copyright__=r"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
"""

def convertColorTable(table):
	"""Converts a Kaitai Struct-parsed color table to a list of matplotlib color maps"""
	cdict={
		"red": [],
		"green": [],
		"blue": []
	}
	countOfColors=len(table.colors)
	maxColorIndex=countOfColors-1
	for i, col in enumerate(table.colors):
		for compName in cdict:
			comp=getattr(col, compName)/255
			cdict[compName].append( (i/maxColorIndex, comp, comp) )
	for compName in cdict:
		cdict[compName]=np.array(cdict[compName])
	return LinearSegmentedColormap(table.title, cdict)

def import256ColorMap(palFileName, index=None):
	raise NotImplementedError("For now parsing .256 palettes is not imiplemented yet.")

def importPalColorMap(palFileName, index=None):
	"""Converts an NT-MDT .pal file into matplotlib colormaps"""
	return convertParsedPalColorMapIntoMatplotlib(kaitaiParseBase(NtMdtPal, palFileName), index)

importFunctionsDispatchDict={
	".pal": importPalColorMap,
#	".256": import256ColorMap
}

def importColorMap(fileName:str, index=None, *args, **kwargs):
	"""Dispatches on importer function depending on pallette extension"""
	ext=os.path.splitext(fileName)[1].lower()
	
	if ext in importFunctionsDispatchDict:
		return importFunctionsDispatchDict[ext](fileName, index, *args, **kwargs)
	else:
		NotImplementedError("For now parsing "+ext+" palettes is not imiplemented yet.")

def convertParsedPalColorMapIntoMatplotlib(parsed, index):
	"""Converts Kaitai Struct parsed colormap into matplotlib colormap"""
	if index is None:
		index=range(len(parsed.tables))
	if isinstance(index, (int, str)):
		index=[index]
	res={"name":{}, "index":{}}
	nameIndex={}
	for i, el in enumerate(index):
		if isinstance(el, int):
			pass
		elif isinstance(el, str):
			if not nameIndex:
				nameIndex={table.title:i for i, table in enumerate(parsed.tables)}
			el=nameIndex[el]
		converted=lazy_object_proxy.Proxy(functools.partial(convertColorTable, parsed.tables[el]))
		res["index"][el]=converted
		res["name"][res["index"][el].name]=converted
	return res
