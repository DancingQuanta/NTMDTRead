NTMDTRead
==========
[![PyPi Status](https://img.shields.io/pypi/v/NTMDTRead.svg)](https://pypi.python.org/pypi/NTMDTRead)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/NTMDTRead.svg?branch=master)](https://travis-ci.org/KOLANICH/NTMDTRead)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/NTMDTRead.svg)](https://coveralls.io/r/KOLANICH/NTMDTRead)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/NTMDTRead.svg)](https://libraries.io/github/KOLANICH/NTMDTRead)

A set of tools to read the files produced by [NT-MDT](http://www.ntmdt-si.ru/) software.

* ```NTMDTReader``` - Reads ```.mdt``` file format. Not very ready: some files are not read at all, some are read incorrectly, in some files images sliced over diagonal and flipped, some frames are not yet implemented. But for large count of files it works pretty fine. Since it is based on the [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) [description](https://github.com/kaitai-io/kaitai_struct_formats/blob/master/scientific/nt_mdt/nt_mdt.ksy) reverse-engineered from [gwyddion implementation](https://svn.code.sf.net/p/gwyddion/code/trunk/gwyddion/modules/file/nt-mdt.c), it is licensed on the terms of [![GNU General Public License v3](https://www.gnu.org/graphics/gplv3-88x31.png)](./gpl-3.0.md). Sorry for that.

* ```colors``` - Reads ```.pal``` palette files and transforms them into ```matplotlib``` colormaps. The format parsing code is based on the Kaitai Struct [description](https://github.com/kaitai-io/kaitai_struct_formats/blob/master/scientific/nt_mdt/nt_mdt_pal.ksy). Its license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

* ```palettes``` - A convenient importer for palettes. You may prefer to use it instead of ```colors```.
```python
from NTMDTRead.palettes.Rainbows import Rainbow1
from NTMDTRead.palettes import Rainbows
import NTMDTRead.palettes.Rainbows
```
Its license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

* ```NTMDTReaderTSV``` - Reads TSV file exported by ```Nova``` or ```ImageAnalysis```. The license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

