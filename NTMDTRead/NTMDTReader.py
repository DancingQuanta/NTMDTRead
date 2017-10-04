import re
import numpy as np
import bs4
import pint
import os
from .nt_mdt import *
from .kaitaiParseBase import kaitaiParseBase

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


ureg = pint.UnitRegistry(default_as_delta=True, autoconvert_offset_to_baseunit=True)
ureg.load_definitions(os.path.join(os.path.split(__file__)[0], "units.txt"))
ureg.default_format = "~P"

#TODO:
# nova has COM interface NT-MDT\Nova\nova.tlb HKEY_LOCAL_MACHINE\SOFTWARE\Classes\TypeLib\{1AFB341D-77DC-4C0C-BD3E-926FE318EB68}\1.0\0\win32

digitRx=re.compile("\d")
def enumNameToUnitName(name:str):
	name=digitRx.sub("", name)
	name=name.replace("_", "")
	return name

unitsEnumPintMapping={}

def unitEnumToPint(enumValue:NtMdt.Unit):
	"""Converts a member of NtMdt.Unit into a ```pint``` unit"""
	if enumValue not in unitsEnumPintMapping:
		unitsEnumPintMapping[enumValue]=ureg.parse_expression(enumNameToUnitName(enumValue.name))
	return unitsEnumPintMapping[enumValue]


class NTMDTReader():
	"""A class to read .mdt files. Wraps Kaitai Struct-generated parser for more convenience."""
	def __init__(self, fileName:str):
		self.parsed=kaitaiParseBase(NtMdt, fileName)
		for fr in self.parsed.frames.frames:
			data=fr.main.frame_data
			if hasattr(data.xml, "xml"):
				data.xml.xml=bs4.BeautifulSoup(fr.main.frame_data.xml.xml, "lxml")
			if hasattr(data, "image") and hasattr(data, "fm_xres") and hasattr(data, "fm_yres"):
				data.image=np.array(fr.main.frame_data.image)
				data.image.shape=(data.fm_xres, data.fm_yres)
				try:
					self.size=(
						(data.fm_xres*data.vars.x_scale.step*unitEnumToPint(data.vars.x_scale.unit)).to_base_units().to_compact(),
						(data.fm_yres*data.vars.y_scale.step*unitEnumToPint(data.vars.y_scale.unit)).to_base_units().to_compact()
					)
				except:
					self.size=(
						data.fm_xres*data.vars.x_scale.step,
						data.fm_yres*data.vars.y_scale.step
					)