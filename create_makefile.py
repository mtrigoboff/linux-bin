#! /usr/bin/python3

from functools import reduce
import os, sys

class Target:
	def __init__(self, name, nameLgth, dependencies):
		self.name =			name
		self.nameLgth =		nameLgth
		self.nTabs =		-1
		self.dependencies =	dependencies

tabWidth =	4
header = 'include ~michael.trigoboff/bin/makeflags_g++\n'
footer = ('.PHONY: x', 'x:', '# clean the directory', 'rm -f *.o')

def createMakefile(projectPath):

	# collect .cpp files and their .h dependencies into cppFiles
	targets = []
	for fileName in os.listdir(projectPath):
		fileNameBase, fileNameExt = os.path.splitext(fileName)
		if fileNameExt == '.cpp':
			filePath = os.path.join(projectPath, fileName)
			cppFile = open(filePath, mode='r')
			lines = cppFile.readlines()
			cppFile.close()
			hdrFiles = []
			for line in lines:
				if line.startswith('#include "'):
					hdrFiles.append(line.split('"')[1])
			targetNameSuffix = '.o' if not fileNameBase.startswith(appTargetNameStart) else ''
			targetName = fileNameBase + targetNameSuffix
			targets.append(Target(targetName, len(targetName) + 1, hdrFiles))
			# +1 for ':' delimiter after targetName in makefile

	# gather .o files needed for asgmt0[1234] rule, add them to dependencies for app
	assert targets[0].name.startswith(appTargetNameStart)
	oFiles = [target.name for target in targets if not target.name.startswith(appTargetNameStart)]
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
	makefile = open(os.path.join(projectPath, 'makefile'), 'w')
	print(header,										file=makefile, sep='')
	for target in targets:

		# print name followed by correct number of tabs
		print(target.name, ':', '\t' * target.nTabs,	file=makefile, end='', sep='')

		# print dependencies
		firstDependent = True
		for dependent in target.dependencies:
			if firstDependent:
				firstDependent = False
			else:
				print(' ',								file=makefile, end='', sep='')
			print(dependent,							file=makefile, end='', sep='')

		# print end of line
		print(											file=makefile,		   sep='')
		print(											file=makefile,		   sep='')

	print(footer[0],									file=makefile,		   sep='')
	print(footer[1],									file=makefile, end='', sep='')
	print('\t' * nTabsMax,								file=makefile, end='', sep='')
	print(footer[2],									file=makefile,		   sep='')
	print('\t' * nTabsMax,								file=makefile, end='', sep='')
	print(footer[3],									file=makefile, end='')
	print(targets[0].name,								file=makefile)

	makefile.close()

if len(sys.argv) < 3:
	print('need to specify folder path, app target name.startswith()')
	sys.exit()

# when invoked from the command line
if __name__ == '__main__':
	projectPath = sys.argv[1]
	appTargetNameStart = sys.argv[2]
	print('makefiles: ', projectPath, appTargetNameStart)
	if os.path.isfile(projectPath):
		print('not a directory')
		sys.exit()
	print(projectPath)
	createMakefile(projectPath)
