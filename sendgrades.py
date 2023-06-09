#!/usr/bin/env python3

# command line arguments: course, assignment, term

# Read lines from tab-delimited text file. First line of file contains column header names
# and is skipped. Uses each line to create email containing grade information.
#
# Tab-delimited text file is produced by Excel, and each line will have all 5 tabs
# that delimit the 6 columns.
#
# Columns are:
#	0: student's last name
#	1: student's first name	
#	2: student's Desire2Learn id, same as Linux email id
#	3: grade for the assignment
#	4: optional comment
#	5: name of file to attach to msg
#	   (currently not implemented, worked in Linux-based version on syccux...)

import datetime, os, os.path, subprocess, sys, textwrap, time

courseGrade = 		'course'
finalExamGrade =	'final'

courseAttrs =	{'cs140u'	:	('lab',		'Lab'		),
			 	 'cs160'	:	('asgmt',	'Assignment'),
				 'cs201'	:	('asgmt',	'Assignment'),
			 	 'cs260'	:	('asgmt',	'Assignment')}

instructorAddr = 		'michael.trigoboff'
serverAddr =			'syccuxas01.pcc.edu'

msgFilePath = os.path.expanduser(os.path.join('~', 'temp', 'msg.txt'))

divider = '-----------------------------------------------------------------'
footer = '\n' + divider + '''
This message was generated automatically by a Python script.
Do not reply to it via standard email. If you need to discuss
your grade for this assignment, send email via MyPCC or D2L.
'''

def duration(start, end):
	runTime = end - start
	minutes = int(runTime / 60)
	if minutes == 1:
		minuteStr = ''
	else:
		minuteStr = 's'
	return '%d minute%s, %.1f seconds' % (minutes, minuteStr, runTime % 60)

# send grades to students' linux email accounts
def sendgrades(course, item, term):
	
	startTime = time.time()

	try:
		[fileNameStr, titleStr] = courseAttrs[course]
	except KeyError:
		print('unknown course')
		sys.exit(-1)

	if item == courseGrade:
		fileNameStr = 'course'
		titleStr = 'Course'
		addNumber = False
	elif item == finalExamGrade:
		fileNameStr = 'final'
		titleStr = 'Final'
		addNumber = False
	else:
		addNumber = True
		
	if addNumber:
		itemNumStr = str(item)
		fileNameStr += '0' + itemNumStr
		titleStr += ' ' + itemNumStr

	print(divider)
	
	nTokenErrors = 0
	nMsgsSent = 0
	monthDay = datetime.datetime.now().strftime('%m-%d')
	gradesFilePath = '/home/inst/' + instructorAddr + '/%s.classes/%s/%s%s%sgrades_%s.txt' \
					  % (course, term, course, term, fileNameStr, monthDay)
	gradesFile = open(gradesFilePath, 'r')

	for line in gradesFile.readlines()[1:]:					# skip first line containing column headers

		tokens = line.split('\t')							# extract tokens from line
		if len(tokens) < 6:
			print('token # error (%d):\n    %s' % (len(tokens), line), end='', file=sys.stderr)
				# line ends in newline, trailing comma tells print not to print the newline
			nTokenErrors += 1
			continue

		# extract tokens from token list
		[lastName, firstName, studentAddr, grade, comment, attachedFileName] = tokens[0:6]
		comment = comment.strip(' "')						# Excel embeds comments containing ',' in "..."
		attachedFileName = attachedFileName.strip(' \n')	# last grade in line will include the '\n'

		# process only lines that have student id's and grades
		if len(studentAddr) > 0 and len(grade) > 0:
			course = course.upper()
			if item == courseGrade:
				msgSubject =	'%s: Course Grade\n'		% (course)
			elif item == finalExamGrade:
				msgSubject =	'%s: Final Exam Grade\n'	% (course)
			else:
				msgSubject =	'%s: %s Grade\n'			% (course, titleStr)
																								
			msgFile = open(msgFilePath, 'w+')
			if item == courseGrade:
				msgFile.write('%s Course Grade\n\n'			% (course))
			elif item == finalExamGrade:
				msgFile.write('%s Final Exam Grade\n\n'		% (course))
			else:
				msgFile.write('%s %s\n\n'					% (course.upper(), titleStr))
			msgFile.write('Grade: %s\n\n'					% (grade))
			if len(comment) > 0:
				msgFile.write('Comment:\n')
				lines = textwrap.wrap(comment, 80)
				for line in lines:
					msgFile.write('%s\n'					% (line))
			msgFile.write(footer)
			msgFile.close()
			msgFile = open(msgFilePath, 'r')
			subprocess.call(['mail', '-s', msgSubject, '-b', instructorAddr, studentAddr], \
							stdin=msgFile)
			msgFile.close()
			print(studentAddr)
			nMsgsSent += 1
			time.sleep(0.1)		# avoid hammering mail service too quickly
			
			# warn if a file attachment was specified
			if len(attachedFileName) > 0:
				print('file attachment: %s' % (attachedFileName), file=sys.stderr)
			
	try:
		os.remove(msgFilePath)
	except FileNotFoundError:
		# file will not be there if no msgs were sent
		pass

	print(divider)

	# report number of lines with token # errors
	if nTokenErrors > 0:
		print('token # errors: %d' %(nTokenErrors), file=sys.stderr)
		print(divider)
		
	endTime = time.time()
	if nMsgsSent == 1:
		nMsgsStr = ''
	else:
		nMsgsStr = 's'
	print('done:     %d message%s sent' % (nMsgsSent, nMsgsStr))
	print('run time:', duration(startTime, endTime))
	print('msgs/sec: %.1f' % ((endTime - startTime) / nMsgsSent))
	print()
			
# if invoked from the command line

coursePrompt =			'course name:      '
asgmtPrompts =			{'cs201' : 'asgmt#, 1 digit:  '}
termPrompt =			'term:             '

if __name__ == '__main__':
	print('Send Grades')
	print(divider)
	if len(sys.argv) < 2:
		course =		input(coursePrompt)
		asgmtPrompt =	asgmtPrompts.get(course, 'assignment/lab #: ')
		item =			input(asgmtPrompt)		# type 'final' for final exam grades
												# type 'course' for course grades
		term =			input(termPrompt)
		print('%s%s' % (coursePrompt, course))
		print('%s%s' % (asgmtPrompt, item))
		print('%s%s' % (termPrompt, term))
	else:
		course =		sys.argv[1]
		item =			sys.argv[2]
		term =			sys.argv[3]
	sendgrades(course, item, term)
