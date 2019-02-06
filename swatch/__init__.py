# encoding: utf-8
"""
swatch, a parser for adobe swatch exchange files
Copyright (c) 2014 Marcos A Ojeda http://generic.cx/

With notes from
http://iamacamera.org/default.aspx?id=109 by Carl Camera and
http://www.colourlovers.com/ase.phps by Chris Williams

All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""


__title__ = 'swatch'
__version__ = '0.4.0'
__author__ = 'Marcos Ojeda'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Marcos A Ojeda'


from . import parser
from . import writer
import struct

HEADER = b'ASEF'
V_MAJOR = 1
V_MINOR = 0

def parse(filename):
    """ Parses a ``.ase`` file and returns a list of colors and color groups
        
        `swatch.parse(…)` reads in an ``.ase`` file and converts it to a list
        of colors and palettes. Colors are ``dict``s of the form
        
        ```json
        {
            'name': 'color name',
            'type': 'Process',
            'data': {
                'mode': 'RGB',
                'values': [1.0, 1.0, 1.0]
            }
        }
        ```
        
        The values provided vary between color mode. For all color modes, the
        value is always a ``list`` of floats. Valid ASE color modes are:
        
        RGB: three floats between [0, 1]  corresponding to RGB.
        CMYK: four floats between [0, 1] inclusive, corresponding to CMYK.
        Gray: one float between [0, 1] with 1 being white, 0 being black.
        LAB: three floats. The first, L, is ranged from [0, 1]. Both A and B are
        floats ranging from [-128.0, 127.0]. I believe Illustrator just crops
        these to whole values, though.
        
        Palettes (née Color Groups in Adobe parlance) are also ``dicts``, but they have an
        item named “swatches” which contains a ``list`` of colors contained within
        the palette.
        
        ```json
        {
            'name': 'accent colors',
            'type': 'Color Group',
            'swatches': [
                {color}, {color}, ..., {color}
            ]
        }
        ```
        
        Because Adobe Illustrator lets swatches exist either inside and outside
        of palettes, the output of swatch.parse is a list that may contain
        swatches and palettes, i.e. `[ swatch* palette* ]`
        
        Here's an example with a light grey swatch followed by a color group,
        containing three colors:
        
            >>> import swatch
            >>> swatch.parse("example.ase")
            [{'data': {'mode': 'Gray', 'values': [0.75]},
              'name': 'Light Grey',
              'type': 'Process'},
             {'name': 'Accent Colors',
              'swatches': [{'data': {'mode': 'CMYK',
                 'values': [0.5279774069786072,
                  0.24386966228485107,
                  1.0,
                  0.04303044080734253]},
                'name': 'Green',
                'type': 'Process'},
               {'data': {'mode': 'CMYK',
                 'values': [0.6261844635009766,
                  0.5890134572982788,
                  3.051804378628731e-05,
                  3.051804378628731e-05]},
                'name': 'Violet Process Global',
                'type': 'Global'},
               {'data': {'mode': 'LAB', 'values': [0.6000000238418579, -35.0, -5.0]},
                'name': 'Cyan Spot (global)',
                'type': 'Spot'}],
              'type': 'Color Group'}]
    """
    with open(filename, "rb") as data:
        header, v_major, v_minor, chunk_count = struct.unpack("!4sHHI", data.read(12))
        
        assert header == HEADER
        assert (v_major, v_minor) == (V_MAJOR, V_MINOR)
        
        return [c for c in parser.parse_chunk(data)]

def dumps(obj):
    """ Converts a swatch to bytes, suitable for writing """
    chunk_count = writer.chunk_count(obj)
    head = struct.pack('!4sHHI', HEADER, V_MAJOR, V_MINOR, chunk_count)
    body = b''.join([writer.chunk_for_object(c) for c in obj])
    return head + body

def dump(obj, handle):
    """ Write a swatch to a python file object """
    handle.write(dumps(obj))

def write(obj, filename):
    """ Write a swatch object to the filename specified
        
        If `filename` exists, it will be overwritten.
        
        `obj` *must* be a list of swatches and palettes, as follows:
        
        ```
            [ swatch* palette* ]
        ```
        
        The best source for descriptions of each of these is to be found
        in the `parser` documentation.
    """
    with open(filename, 'wb') as handle:
        dump(obj, handle)
