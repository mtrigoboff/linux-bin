#!/usr/bin/env python

# recursively deletes *.exe

import os, sys				# import Python standard modules
import deleteexe, walktree	# import our own modules

if len(sys.argv) < 2:
	dir = '.'
else:
	dir = sys.argv[1]
print 'deleted the following files:'
walktree.walk(os.path.realpath(dir), deleteexe.delete)
