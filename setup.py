#!/usr/bin/env python3
import os
from setuptools import setup
from setuptools.config import read_configuration

cfg = read_configuration('./setup.cfg')
#print(cfg)
cfg["options"].update(cfg["metadata"])
cfg=cfg["options"]

from kaitaiStructCompile.toolkit import permissiveDecoding
from pathlib import Path
formatsPath=Path(__file__).parent / "kaitai_struct_formats"
mdtFormatsDir=formatsPath / "scientific" /"nt_mdt"
cfg["kaitai"]={
	"formatsRepo": {
		"localPath" : str(formatsPath),
		"update": True
	},
	"outputDir": "NTMDTRead",
	"inputDir": mdtFormatsDir,
	"formats":{},
	"search": True
}

setup(use_scm_version = True, **cfg)
