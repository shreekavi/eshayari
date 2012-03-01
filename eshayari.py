#!/usr/bin/env python

import os
import sys
import gobject
gobject.threads_init()

import eshayari
eshayari.main.main(sys.argv[1:])

g_loop = threading.Thread(target=gobject.MainLoop().run)
g_loop.daemon = True
g_loop.start()