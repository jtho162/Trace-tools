#!/usr/bin/python
import re
from sys import argv

class colors:
	lightblue = "\033[1;36m"
	blue = "\033[1;34m"
	normal = "\033[0;00m"
	red = "\033[1;31m"
	white = "\033[1;37m"
	green = "\033[1;32m"

banner = "\n " + "-" * 72 + "\n " + colors.white + " nmapparse 1.0 - Nmap Output Parser, Alton Johnson (alton.jx@gmail.com)\n " + colors.normal + "-" * 72 + "\n "

def help():
	print banner
	print " Usage: ./nmapparse.py results.gnmap"
	print "\n Note: This script must point to a grepable output file from nmap to work properly.\n"
	exit()

def start(argv):
	if len(argv) == 0:
		help()
	contents = sorted(open(argv[0]).read().split('\n'))
	data = []

	class colors:
		blue = "\033[1;34m"
		normal = "\033[0;00m"

	for item in contents:
		ip_addr = item[item.find(":")+2:item.find("(")-1]
		info = re.findall("(?<=Ports: )(.*?)(?=Ignored)", item)
		if len(info) == 0:
			info = re.findall("(?<=Ports: )(.*?)(?=Seq Index)", item)
		if len(info) == 0:
			info = re.findall("(?<=Ports: )(.*?)(?=$)", item)
		if len(info) != 0:
			for i in info:
				result = i.split(',')
				for x in result:
					port = re.findall("([0-9]+/open/.*?)/", x)
					if "[]" in str(port):
						continue
					port = port[0].replace("/open", "")
					service = re.findall("(?<=//)(.*?)(?=/)", x)[0]
					version = x.split("/")[-2]
					if len(version) > 40:
						version = version[:40]
					if len(version) == 0:
						version = "-"
					data.append([ip_addr, port, service, version])


	#grab offset
	offset = [0,0,0,0]
	for row in data:
		for num in range(0,len(row)):
			if len(row[num]) > offset[num]:
				offset[num] = len(row[num])

	#print pretty lines
	row_lines = " +" + "-" * (offset[0]+3) + "+" + "-" * (offset[1]+3) + "+" + \
	"-" * (offset[2]+3) + "+" + "-" * (offset[3]+3) + "+"

	print
	print row_lines
	print " | " + colors.blue + "IP Address " + colors.normal + \
	" " * (offset[0]-9) + "|" + colors.blue + " Port" + colors.normal + \
	" " * (offset[1]-2) + "|" + colors.blue + " Service" + colors.normal + \
	" " * (offset[2]-5) + "|" + colors.blue + " Version" + colors.normal + " " * (offset[3]-5) + "|"

	#output
	ip = ''
	for line in data:
		if line[0] != ip:
			print row_lines
			ip = line[0]
		for num in range(0,len(line)):
			print " | " + line[num] + (" " * (offset[num]-len(line[num]))), 
		print " |"

	print row_lines
	print
try:
	start(argv[1:])
except Exception, err:
	print err
