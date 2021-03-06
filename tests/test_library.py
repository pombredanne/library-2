'''

test.py: Python testing to ensure correct formatting and varibles included for
         metadata in experiments.

The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat, Stanford University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os
import re
import sys
from glob import glob
from expfactory.logger import bot
from expfactory.utils import read_json
import json

from expfactory.validator import (
    LibraryValidator,
    ExperimentValidator,
    RuntimeValidator
)
from unittest import TestCase

VERSION = sys.version_info[0]
here = os.getcwd()

print("*** PYTHON VERSION %s BASE TESTING START ***" %(VERSION))

class TestLibrary(TestCase):

    def setUp(self):

        self.LibValidator = LibraryValidator()
        self.ExpValidator = ExperimentValidator()
        self.RuntimeValidator = RuntimeValidator()
        self.experiments_base = "%s/experiments" %(here) 
        self.experiments = glob("%s/*" %self.experiments_base)
        
    def test_library(self):
        '''test_validate_library calls all subfunctions
        '''
        print("...Test: Global Library validation")
        for jsonfile in self.experiments:
            self.assertTrue(self.LibValidator.validate(jsonfile))
        
    def test_single_experiments(self):
        '''test_load_json ensures that all files load
        '''
        for jsonfile in self.experiments:
            print("...%s" %os.path.basename(jsonfile))
            config = read_json(jsonfile)
            self.assertTrue('github' in config)
            self.assertTrue(isinstance(config,dict))
            url = config['github']
            self.assertTrue(self.ExpValidator.validate(url))

    def test_previews(self):
        '''assert that each experiment is previewed at the Github page
           where served
        '''
        bot.test('Testing experiment previews...')
        for jsonfile in self.experiments:
            experiment = os.path.basename(jsonfile)
            print("...%s experiment preview?" %experiment)
            config = read_json(jsonfile)
            self.assertTrue('github' in config)
            self.assertTrue(isinstance(config,dict))
            url = config['github']
            result = self.RuntimeValidator.validate(url)
            print(result)
            print(url)        
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
