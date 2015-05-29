#!/usr/bin/env python

import imp, sys
module = sys.argv[1]

try:
    imp.find_module(module)
    found = True
except ImportError:
    found = False

print found
