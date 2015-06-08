# script
import sys, os
import json, time
import xml.etree.ElementTree as ET
import base64
import lxml.etree as etree

from array import array
from types import *
from html.parser import HTMLParser
from optparse import OptionParser

class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0 
		self.data = []
		self.test = []
		self.testArray = []
		self.testUUIDA=0
		self.testUUIDB=0
		self.testSeq=0

	def handle_starttag(self, tag, attrs):
		self.recording = 1
		self.data=''
		for attr in attrs:
			tmp=attr[1].split('"')
			if tmp[0]=="javascript:editParameter(":
				self.testSeq=int(tmp[1]) #test sequence

	def handle_endtag(self, tag):
		self.recording -= 1

	def handle_data(self, data):
		self.testArray.append([self.testSeq,self.recording,data])

def main():
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	rule = []

	for rule in root.findall('custom_rule'):
		parser = MyHTMLParser()
		ruleUUID=rule.find('uuid').text
		detailedRuleData=base64.b64decode(rule.find('rule_data').text)
		x = etree.fromstring(detailedRuleData)
		m = etree.tostring(x, pretty_print = True)
		drdroot = ET.fromstring(detailedRuleData)
		testDefinitions=drdroot.find('testDefinitions')
		for elTests in testDefinitions.findall('test'):
			testName=elTests.get('name')
			testUUID=elTests.get('uid')
			ruleText=str(elTests.find('text').text)
			if isinstance(ruleText, str):
				parser.close()
				parse=str(parser.feed(ruleText))
		prttest=''
		oldx0=0
		for x in parser.testArray:
			if str(x[0])!=oldx0: 
				prttest=prttest+' AND '
				oldx0=str(x[0])
			prttest=prttest+str(x[2])
		print(drdroot.find('name').text,drdroot.get('type'),drdroot.get('enabled'),drdroot.find('notes').text, sep='#',end='\n')

if __name__ == "__main__":
    main()
