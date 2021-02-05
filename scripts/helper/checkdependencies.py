#!/bin/python3

import sys
import os

if '-h' in sys.argv : sys.exit('{}\n{}\n\t{}'.format(
	'First argument can be specified to provide the path to the modules folder if they are not in a default one',
	'Now your paths are :',
	'\n\t'.join(sys.path)
))

#LINUX PACKAGES
if int(os.system('ethtool --version 1>/dev/null 2>/dev/null')) != 0: print('Package : ethtool : Check failed')
else : print('Package : ethtool : OK')

if int(os.system('tshark -v 1>/dev/null 2>/dev/null')) != 0: print('Package : tshark : Check failed')
else : print('Package : tshark : OK')

if int(os.system('awk 1>/dev/null 2>/dev/null')) != 0: print('Package : awk : Check failed')
else : print('Package : awk : OK')

#PYTHON PACKAGES
def failure(package_name):
	print('Module : {} : Failed to import'.format(package_name))
def success(package_name):
	print('Module : {} : OK'.format(package_name))
def imp(package_name):
	try : __import__(package_name)
	except :
		failure(package_name)
		return False
	else :
		success(package_name)
		return True

#Python modules
required_modules = [
	're',
	'os',
	'math',
	'datetime',
	'argparse',
	'ipaddress',
	'numpy',
	'termcolor',
	'pickle',
	'scapy',
	'sklearn',
	'matplotlib'
]
results = [imp(m) for m in required_modules]


if len(sys.argv) >= 2 : sys.path.insert(0, sys.argv[1])
custom_modules = [
	'packet',
	'anonymizer',
	'splitter',
	'dataStructure',
	'clsModel',
	'easycolor'
]
custom_results = [imp(m) for m in custom_modules]


if False in results:
	try :
		from easycolor import ecprint
		ecprint('Error in required modules : Some modules could not be imported', c = 'red')
	except : print('Error in required modules : Some modules could not be imported')

if False in custom_results:
	try :
		from easycolor import ecprint
		ecprint('Error in custom modules : Try providing the absolute path to the custom modules folder as argument', c = 'red')
	except : print('Error in custom modules : Try providing the absolute path to the custom modules folder as argument')

if (not False in results) and (not False in custom_results):
	from easycolor import ecprint
	ecprint('Check passed without errors', c = 'green')
