# encoding: utf-8
"""
swatch, a parser for adobe swatch exchange files
Copyright (c) 2014 Marcos A. Ojeda http://generic.cx/

With notes from:
• http://iamacamera.org/default.aspx?id=109 and
• http://www.colourlovers.com/ase.phps

All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""
import logging
import struct
import os


def parse_chunk(handle):
    """ Generate object dicts for arbitrary chunks, until the
        filehandle `handle` has been exhausted.
    """
    chunk_type = handle.read(2)
    
    while chunk_type:
        if chunk_type == b'\x00\x01':
            # a single color
            logging.debug("[swatch.parser] parse_chunk saw single color")
            out = dict_for_chunk(handle)
            yield out
        
        elif chunk_type == b'\xC0\x01':
            # folder/palate
            logging.debug("[swatch.parser] parse_chunk saw folder")
            out = dict_for_chunk(handle)
            out['swatches'] = [x for x in colors(handle)]
            yield out
        
        elif chunk_type == b'\xC0\x02':
            # this signals the end of a folder
            logging.debug("[swatch.parser] parse_chunk saw end of folder")
            assert handle.read(4) == b'\x00\x00\x00\x00'
            pass
        
        else:
            # the file is malformed?
            logging.debug("[swatch.parser] parse_chunk got malformed ase file")
            assert chunk_type in [
                b'\xC0\x01', b'\x00\x01', b'\xC0\x02', b'\x00\x02']
            pass
        
        chunk_type = handle.read(2)


def colors(handle):
    """ Generate object dicts for all continuously found color chunks """
    chunk_type = handle.read(2)
    while chunk_type in [b'\x00\x01', b'\x00\x02']:
        out = dict_for_chunk(handle)
        yield out
        chunk_type = handle.read(2)
    handle.seek(-2, os.SEEK_CUR)

COLOR_TYPES = ('Global', 'Spot', 'Process')
COLOR_MODES = { b'RGB'  : '!fff',
                b'Gray' : '!f',
                b'CMYK' : '!ffff',
                b'LAB'  : '!fff' }

def dict_for_chunk(handle):
    """ Return a dict with decoded information for a single chunk """
    chunk_length = struct.unpack(">I", handle.read(4))[0]
    data = handle.read(chunk_length)
    
    title_length = 2 + ((struct.unpack(">H", data[:2])[0]) * 2)
    title = data[2:title_length].decode("utf-16be").strip('\0')
    color_data = data[title_length:]
    
    output = {
        'name': str(title),
        'type': 'Color Group'  # default to color group
    }
    
    if color_data:
        color_mode = struct.unpack("!4s", color_data[:4])[0].strip()
        color_values = list(struct.unpack(COLOR_MODES[color_mode], color_data[4:-2]))
        
        swatch_type_index = struct.unpack(">h", color_data[-2:])[0]
        swatch_type = COLOR_TYPES[swatch_type_index]
        
        output.update({
            'data': {
                'mode': color_mode.decode('utf-8'),
                'values': color_values
            },
            'type': str(swatch_type)
        })
    
    return output
