#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import requests
import json
import math
from bs4 import BeautifulSoup

try:
    string_type = basestring
except NameError:
    string_type = str

def hex2rgb(h):
    """ Convert a hex string or number to an RGB triple """
    # q.v. https://git.io/fh9E2
    if isinstance(h, string_type):
        return hex2rgb(int(h[1:] if h.startswith('#') else h, 16))
    return (h >> 16) & 0xff, (h >> 8) & 0xff, h & 0xff

def compand(v):
    """ Compand a linearized value to an sRGB byte value """
    # q.v. http://www.brucelindbloom.com/index.html?Math.html
    V = (v <= 0.0031308) and (v * 12.92) or ((1.055 * math.pow(v, 1 / 2.4)) - 0.055)
    return V * 255.0

def uncompand(A):
    """ Uncompand an sRGB byte value to a linearized value """
    # q.v. http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    V = A / 255.0
    return (V <= 0.04045) and (V / 12.92) or math.pow(((V + 0.055) / 1.055), 2.4)

def tds_to_dictionary(tds):
    """ Package the scraped XTerm color data as a dictionary """
    # q.v. https://jonasjacek.github.io/colors/
    out = dict(xterm_number=int(tds[1].contents[0]),
               name=tds[2].contents[0].strip(),
               hex=tds[3].contents[0].strip(),
               rgb_string=tds[4].contents[0].strip(),
               hsl_string=tds[5].contents[0].strip(),
               rgb=hex2rgb(tds[3].contents[0].strip()))
    return out

def scraped_to_ase(scraped_color):
    """ Convert a scraped XTerm color dictionary to an ASE dictionary """
    # q.v https://github.com/fish2000/swatch/blob/master/README.rst
    assert 'name' in scraped_color
    assert 'rgb' in scraped_color
    values = [uncompand(A) for A in scraped_color['rgb']]
    out = dict(name=scraped_color['name'],
               type='Process',
               data=dict(mode='RGB', values=values))
    return out

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    scraped = {}
    output = { 'name'       : 'XTerm Colors',
               'type'       : 'Color Group',
               'swatches'   : [] }
    
    # get all table rows:
    alltrs = soup.findAll(name='tr')
    
    # first row is the header, skip it
    trs = alltrs[1:]
    assert len(trs) == 256
    
    for tr in trs:
        tds = tuple(tr.children)
        assert len(tds) == 6
        color_dict = tds_to_dictionary(tds)
        scraped.update({ color_dict.get('name') : color_dict })
    
    # print(json.dumps(scraped, indent=4))
    
    for infodict in scraped.values():
        output['swatches'].append(scraped_to_ase(infodict))
    
    print(json.dumps(output, indent=4))
    

URL = 'https://jonasjacek.github.io/colors/'

if __name__ == '__main__':
    scrape(URL)
