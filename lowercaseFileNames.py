import os, sys

if len(sys.argv) < 2:
	print('need to specify folder path')
	sys.exit()

print('lowercase file names\n')
dirPath = sys.argv[1]
#dirPath = os.path.join('.', 'test')
for projectDirName in os.listdir(dirPath):
	projectPath = os.path.join(dirPath, projectDirName)
	if os.path.isfile(projectPath):
		continue
	print(projectDirName)
	for fileName in os.listdir(projectPath):
		os.rename(os.path.join(projectPath, fileName), os.path.join(projectPath, fileName.lower()))
