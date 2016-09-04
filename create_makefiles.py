#! /usr/bin/python3

import os, sys
import create_makefile

def createMakefiles(projectsDirPath, appTargetName):
	for projectDirName in os.listdir(projectsDirPath):
		if not os.path.isdir(os.path.join(projectsDirPath, projectDirName)):
			continue
		if projectDirName == '.hg':
			continue
		create_makefile.createMakefile(os.path.join(projectsDirPath, projectDirName), appTargetName)

# when invoked from the command line
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('command line args: projectsDirectoryPath appTargetName')
		sys.exit()
	projectsDirPath = sys.argv[1]
	appTargetName = sys.argv[2]
	print('create_makefiles: ', os.path.abspath(projectsDirPath), appTargetName)
	if os.path.isfile(projectsDirPath):
		print(projectsDirPath, 'is not a directory')
		sys.exit()
	createMakefiles(projectsDirPath, appTargetName)
