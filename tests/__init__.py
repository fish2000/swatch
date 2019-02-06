# encoding: utf-8
"""
swatch.tests

Solarized color palette using LAB data from
http://ethanschoonover.com/solarized

Copyright (c) 2014 Marcos A. Ojeda http://generic.cx/
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
        # self.assertEqual(js, ase, "XTerm colors compare unequal in parser test")
        numpy.testing.assert_almost_equal([item['data']['values'] for item in js[0]['swatches']],
                                          [item['data']['values'] for item in ase[0]['swatches']])

class TestSwatchWriter(unittest.TestCase):
    """ Tests for writer.py """
    
    def setUp(self):
        super(TestSwatchWriter, self).setUp()
        self.maxDiff = 1000
    
    def compare_with_ase(self, basepath):
        import swatch, os, json
        base = os.path.join("tests", "fixtures", basepath)
        with open(base + ".json") as swatch_data:
            generated_ase = swatch.dumps(json.load(swatch_data))
        with open(base + ".ase", 'rb') as raw_ase:
            return raw_ase.read(), generated_ase
    
    def test_single_swatch(self):
        raw, generated = self.compare_with_ase("white swatch no folder")
        self.assertEqual(raw, generated, "single swatch has broken")
    
    def test_LAB(self):
        raw, generated = self.compare_with_ase("solarized")
        self.assertEqual(raw, generated, "LAB test fails with solarized data")
    
    def test_empty_file(self):
        raw, generated = self.compare_with_ase("empty white folder")
        self.assertEqual(raw, generated, "empty named folder no longer writes")
    
    def test_single_swatch_in_folder(self):
        raw, generated = self.compare_with_ase("single white swatch in folder")
        self.assertEqual(raw, generated, "folder with one swatch no longer writes")
    
    def test_RGB(self):
        raw, generated = self.compare_with_ase("sampler")
        self.assertEqual(raw, generated, "RGB writer test fails with sampler")
    
    def test_xterm_colors(self):
        raw, generated = self.compare_with_ase("xterm colors")
        self.assertEqual(raw, generated, "XTerm colors compare unequal in writer test")

if __name__ == '__main__':
    unittest.main()
