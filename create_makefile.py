#! /usr/bin/python3

import os, sys
from functools	import reduce

class Target:
	def __init__(self, name, nameLgth, dependencies):
		self.name =			name
		self.nameLgth =		nameLgth
		self.nTabs =		-1
		self.dependencies =	dependencies

tabWidth =	4
header = 'include ~michael.trigoboff/bin/makeflags_g++\n'
footer = ('.PHONY: x', 'x:', '# clean the directory', 'rm -f *.o ')
	# trailing space in footer[3] is necessary

def createMakefile(projectDirPath):

	# collect .cpp files and their .h dependencies into cppFiles
	targets = []
	for fileName in os.listdir(projectDirPath):
		fileNameBase, fileNameExt = os.path.splitext(fileName)
		if fileNameExt == '.cpp':
			filePath = os.path.join(projectDirPath, fileName)
			cppFile = open(filePath, mode='r')
			lines = cppFile.readlines()
			cppFile.close()
			hdrFiles = []
			for line in lines:
				if line.startswith('#include "'):
					hdrFiles.append(line.split('"')[1])
			targetNameSuffix = '.o' if not fileNameBase == appTargetName else ''
			targetName = fileNameBase + targetNameSuffix
			targets.append(Target(targetName, len(targetName) + 1, hdrFiles))
				# +1 for ':' delimiter after targetName in makefile

	# gather .o files needed for asgmt0[1234] rule, add them to dependencies for app
	assert targets[0].name == appTargetName
	oFiles = [target.name for target in targets if not target.name == appTargetName]
	targets[0].dependencies = oFiles + targets[0].dependencies

	# compute max number of tabs needed for any target
	maxLgthTarget = \
		targets[0] if len(targets) == 1 \
			else reduce(lambda x, y: Target(None, max(x.nameLgth, y.nameLgth), None), targets)
	maxTargetLgth = maxLgthTarget.nameLgth + 1		# +1 for ':' delimiter in makefile rule
	nTabsMax = int(maxTargetLgth / tabWidth) + 1	# +1 so we have at least 1 tab

	# compute number of tabs needed for each target
	for target in targets:
		target.nTabs = nTabsMax - int(target.nameLgth / 4)

	# write makefile

	makefile = open(os.path.join(projectDirPath, 'makefile'), 'w')

	# print identifying comment
	print('# generated for', os.path.abspath(projectDirPath), \
														file=makefile, end='\n\n')

	# print include statement
	print('# C++ compiler flags',						file=makefile)
	print(header,										file=makefile,		   sep='')

	for target in targets:

		# print name followed by ':' and correct number of tabs
		print(target.name, ':', '\t' * target.nTabs,	file=makefile, end='', sep='')

		# print dependencies
		firstDependent = True
		for dependent in target.dependencies:
			if firstDependent:
				firstDependent = False
			else:
				print(' ',								file=makefile, end='', sep='')
			print(dependent,							file=makefile, end='', sep='')

		# print 2 newlines
		print('\n' * 2,									file=makefile, end='', sep='')

	# print phony target
	print(footer[0],									file=makefile,		   sep='')
	print(footer[1],									file=makefile, end='', sep='')
	print('\t' * nTabsMax,								file=makefile, end='', sep='')
	print(footer[2],									file=makefile,		   sep='')
	print('\t' * nTabsMax,								file=makefile, end='', sep='')
	print(footer[3],									file=makefile, end='', sep='')
	print(targets[0].name,								file=makefile)

	makefile.close()

# when invoked from the command line
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('command line args: projectDirectoryPath appTargetName')
		sys.exit()
	projectDirPath = sys.argv[1]
	appTargetName = sys.argv[2]
	print('makefiles: ', projectDirPath, appTargetName)
	if os.path.isfile(projectDirPath):
		print('not a directory')
		sys.exit()
	print(projectDirPath)
	createMakefile(projectDirPath)
