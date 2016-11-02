#!/usr/bin/env python3

# Desire2Learn provides student work in the form of a directory
# containing files of the form: studentName-dateTime-fileName.
#
# This code takes a Desire2Learn directory and creates a subdirectory
# for each student, moves that student's file into the student directory,
# and renames the file to its original name. In other words, this code
# takes each file and creates folder studentName containing file fileName.
#
# This code is intended to work in the situation where students are
# allowed to submit one file only. If a student has submitted more than
# one file, files encountered after the first one will be placed in
# the student's folder with the original Desire2Learn file name.
#
# by Michael Trigoboff, http://spot.pcc.edu/~mtrigobo

import os, shutil, sys, zipfile

homeDirPath =			'/home/inst/michael.trigoboff'
dividerWidth =			20
dividerStudentName =	''

def printDivider(label = '', char = '-', skipLine = False, dividerWidth = 20):
	divider = ''
	if label == '':
		for _ in (range(dividerWidth - len(dividerStudentName) - 2)):
			divider += char
	else:
		charsWidth = dividerWidth - len(label) - 2
		leftWidth = rightWidth = charsWidth / 2
		if charsWidth % 2:
			rightWidth += 1
		for _ in (range(int(leftWidth))):
			divider += char
		divider += ' ' + label + ' '
		for _ in range(int(rightWidth - len(dividerStudentName) - 2)):
			divider += char
	if dividerStudentName == '':
		divider += char + char
	else:
		divider += '<' + dividerStudentName + '>'
	print(divider)
	if skipLine:
		print()

def expandZipFile(zipFileDirPath, zipFilePath):
	zf = zipfile.ZipFile(zipFilePath, 'r')
	zf.extractall(zipFileDirPath)
	zf.close()

def d2lExpandFile():
	
	print('Expand D2L File')
	printDivider()
	
	# get info for file to expand
	course =	input('course name: ')
	asgmt =		input('asgmt name:  ')
	term =		input('term:        ')

	printDivider()
	termDirPath = os.path.join(homeDirPath, course + '.classes', term)
	asgmtDirPath = os.path.join(termDirPath, asgmt)
	zipFileName = asgmt + '.zip'
	zipFilePath = os.path.join(termDirPath, zipFileName)
	if not os.path.isfile(zipFilePath):
		print('%s: file not found' % zipFilePath)
		return
	if os.path.isdir(asgmtDirPath):
		if input('previously expanded: remove? ') == 'y':
			shutil.rmtree(asgmtDirPath)
	
	print('expanding:', zipFileName)
	os.mkdir(asgmtDirPath)
	expandZipFile(asgmtDirPath, zipFilePath)
		
	printDivider()
	nProjects = 0
	for d2lFileName in os.listdir(asgmtDirPath):
		d2lFilePath = os.path.join(asgmtDirPath, d2lFileName)
		if os.path.isfile(d2lFilePath):
			nameComponents = d2lFileName.split('-')
			if len(nameComponents) != 5:	# avoid choking on index.html file
				continue
			studentName = nameComponents[2].strip(' ')
			fileName = nameComponents[4]
			studentDirPath = os.path.join(asgmtDirPath, studentName)
			if not os.path.isdir(studentDirPath):
				print(studentName)
				os.mkdir(studentDirPath)
				studentFilePath = os.path.join(studentDirPath, fileName)
				shutil.move(d2lFilePath, studentFilePath)
				print('   ' + os.path.split(studentFilePath)[1], sep='')
				nProjects += 1
			else:
				shutil.move(d2lFilePath, os.path.join(studentDirPath, d2lFileName))
				print('   additional file', d2lFileName, file=sys.stderr)
	
	printDivider()
	print('%s projects' % (nProjects))
	printDivider('done', '-', False, dividerWidth)

# when invoked from the command line
if __name__ == '__main__':
	d2lExpandFile()
