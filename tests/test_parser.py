# encoding: utf-8
"""
swatch.tests.test_parser

Solarized color palette using LAB data from
http://ethanschoonover.com/solarized

Copyright (c) 2019 Marcos A. Ojeda http://generic.cx/
All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""
from __future__ import print_function

import pytest
import unittest

class TestSwatchParser(unittest.TestCase):
    """ Tests for parser.py """
    
    def setUp(self):
        super(TestSwatchParser, self).setUp()
        self.maxDiff = 10000
    
    def compare_with_json(self, basepath):
        import swatch, os, json
        base = os.path.join("tests", "fixtures", basepath)
        with open(base + ".json") as handle:
            ase = swatch.parse(base + ".ase")
            js = json.load(handle)
            return js, ase
    
    def test_single_swatch(self):
        js, ase = self.compare_with_json("white swatch no folder")
        self.assertEqual(js, ase, "single swatch no longer parses")
    
    def test_LAB(self):
        js, ase = self.compare_with_json("solarized")
        self.assertEqual(js, ase, "LAB test fails with solarized data")
    
    def test_empty_file(self):
        js, ase = self.compare_with_json("empty white folder")
        self.assertEqual(js, ase, "empty named folder no longer parses")
    
    def test_single_swatch_in_folder(self):
        js, ase = self.compare_with_json("single white swatch in folder")
        self.assertEqual(js, ase, "folder with one swatch no longer parses")
    
    def test_RGB(self):
        js, ase = self.compare_with_json("sampler")
        self.assertEqual(js, ase, "RGB parser test fails with sampler")
    
    def test_xterm_colors(self):
        numpy = pytest.importorskip('numpy')
        js, ase = self.compare_with_json("xterm colors")
        assert len(js[0]['swatches']) == 256
        assert len(ase[0]['swatches']) == 256
        numpy.testing.assert_almost_equal([item['data']['values'] for item in js[0]['swatches']],
                                          [item['data']['values'] for item in ase[0]['swatches']])
        numpy.testing.assert_allclose([item['data']['values'] for item in js[0]['swatches']],
                                      [item['data']['values'] for item in ase[0]['swatches']])
        js[0]['swatches'] = []
        ase[0]['swatches'] = []
        self.assertEqual(js, ase, "XTerm color dict stubs compare unequal in parser test")

if __name__ == '__main__':
    unittest.main()
