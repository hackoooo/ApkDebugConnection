#!/usr/bin/env python

import sys
import subprocess
import re
import threading
import ConfigParser


AAPT = ''
ADB = ''
targetPort=8800

packageName = ''
lauchActivity = ''

class TimeoutCommand(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self,timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()

def readConfig(file):
    cf = ConfigParser.ConfigParser()
    cf.read(file)
    global AAPT
    global ADB
    global targetPort
    AAPT = cf.get('config','aapt')
    ADB = cf.get('config','adb')
    targetPort = cf.get('config','targetport')


def getPackageInfo(apkPath):
	global packageName
	global lauchActivity
	cmd = '{aapt} dump badging {apk}'.format(aapt=AAPT, apk=apkPath)
	output = subprocess.check_output(cmd, shell=True)

	package = re.compile(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'")
	lauch = re.compile(r"launchable-activity: name='([^']+)'")

	for line in output.split('\n'):
		pm = package.match(line)
		lm = lauch.match(line)
		if pm:
			packageName,versionCode,versionName = pm.groups()
		elif lm:
			lauchActivity = lm.group(1)
			break
def main(argv):
        readConfig('env.conf')
	getPackageInfo(argv[1])

	print packageName
	print lauchActivity
	index = len(packageName)
	lauch = lauchActivity[:index] + '/' + lauchActivity[index:]

	cmd = '{adb} shell am start -D -S -W {activity}'.format(adb=ADB, activity=lauch)
	print cmd
	timeoutCmd = TimeoutCommand(cmd)
	timeoutCmd.run(3)

	cmd = '{adb} shell ps|grep {pk}'.format(adb=ADB, pk=packageName)
	print cmd

	pro = subprocess.check_output(cmd, shell=True)
	print pro

	pid = re.split(r' +', pro )[1]
	print pid

	cmd = '{adb} forward tcp:{targetPort} jdwp:{targetPid}'.format(adb=ADB, targetPort=targetPort, targetPid=pid)
	print cmd
	print subprocess.check_output(cmd, shell=True)



if __name__ == '__main__':
        main(sys.argv)

