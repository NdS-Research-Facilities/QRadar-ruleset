# python3 script
import sys, os
import json, time
import xml.etree.ElementTree as ET
import base64
import lxml.etree as etree

from array import array
from types import *
from html.parser import HTMLParser
from optparse import OptionParser

import pprint

class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0 
		self.data = []
		self.test = []

	def handle_starttag(self, tag, attrs):
		self.recording = 1
		self.data=''

	def handle_endtag(self, tag):
		self.recording -= 1

	def handle_data(self, data):
		self.testArray.append([testSeq,self.recording,data])

def main():
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	rule = []
	htmlout=['<style type="text/css">\
table.sample {\
	page-break-inside: avoid;page-break-before:auto\
	padding: 5px 20px 5px 0px;\
	border-spacing: 0px;\
	border-style: none;\
	border-collapse: collapse;\
	border-bottom: 1px solid #777\
	border-right: 0px solid #000;\
	border-left: 0px solid #000;\
	border-top: 1px solid #777;\
	background-color: white;\
	text-align: left; \
	font-size:10px; font-family: Arial, Helvetica, sans-serif\
}\
\
table.sample b {\
	color:#749a56; font-size:10px; font-family: Arial, Helvetica, sans-serif\
}\
table.sample h3 {\
	color:#bc232a; font-size:10px; font-family: Arial, Helvetica, sans-serif\ #No\
}\
table.sample h4 {\
	color:#749a56; font-size:10px; font-family: Arial, Helvetica, sans-serif\ #Yes\
}\
\
table.sample th {\
	padding: 5px 20px 5px 0px;\
	border-color: gray;\
	background-color: #749a56;\
	text-allign: left;\
	-moz-border-radius: ;\
	border-bottom: 1px solid #777\
	border-right: 0px solid #000;\
	border-left: 0px solid #000;\
	border-top: 1px solid #777;\
}\
table.sample tr {\
	page-break-inside: avoid;page-break-before:auto\
	padding: 5px 20px 5px 0px;\
	background-color: white;\
	vertical-align: top; \
	-moz-border-radius: ;\
	border-bottom: 1px solid #555\
	border-right: 0px solid #000;\
	border-left: 0px solid #000;\
	border-top: 1px solid #555;\
}\
table.sample td {\
	padding: 10px 20px 10px 0px;\
}\
</style>\
\
<table class="sample">\
    <tr>\
        <th>Rule Name</th>\
        <th>Type</th>\
        <th>Enabled</th>\
        <th>Description</th>\
        <th>Rule</th>\
    </tr>\
\
\
']

	global testSeq

	for rule in root.findall('custom_rule'):
		prtTestArray=[]
		fullTestArray=[]
		htmlTestArray=[]
		parser = MyHTMLParser()
		ruleUUID=rule.find('uuid').text
		detailedRuleData=base64.b64decode(rule.find('rule_data').text)
		x = etree.fromstring(detailedRuleData)
		m = etree.tostring(x, pretty_print = True)
		drdroot = ET.fromstring(detailedRuleData)
		testDefinitions=drdroot.find('testDefinitions')

		ruleEnabled=drdroot.get('enabled')
		if ruleEnabled=='true':
			htmlruleEnabled='<h4>Yes</h4>'
		else:
			htmlruleEnabled='<h3>No</h3>'

		htmlout.append('<tr>')

		negateTextA=''
		negateTextB=''
		testSeq=-1
		for elTests in testDefinitions.findall('test'):
			testSeq=testSeq+1
			testName=elTests.get('name')
			testUUID=elTests.get('uid')
			testNegate=str(elTests.get('negate'))
			ruleText=str(elTests.find('text').text)
			htmltest=''
			if testNegate=="true":
				prttest=negateTextA
				htmltest='<p><b>'+negateTextA+'</b>'
			else:
				prttest=negateTextB
				htmltest='<p><b>'+negateTextB+'</b>'

			negateTextA='AND NOT '
			negateTextB='AND '

			if isinstance(ruleText, str):
				parser.close()
				parser.testArray=[]
				parse=str(parser.feed(ruleText))

			oldx0=-1
			oldx1=-1
			for x in parser.testArray:
				fullTestArray.append(x)
				if str(x[0])!=oldx0: 
					oldx0=str(x[0])
				if str(x[1])!=oldx1: 
					oldx1=int(x[1])
					if oldx1==1:
						htmltest=htmltest+'<b>'
#					else:
#						htmltest=htmltest+'</b>'
				prttest=prttest+str(x[2])
				htmltest=htmltest+str(x[2])+'</b>'
			
			prtTestArray.append(prttest)
			htmlTestArray.append(htmltest)

		#print(prtTestArray)
		#print(fullTestArray)
#		htmlout.append('<td>'+drdroot.find('name').text+'</td><td>'+ruleUUID+'</td><td>'+drdroot.get('type')+'</td><td>'+htmlruleEnabled+'</td><td>'+str(drdroot.find('notes').text)+'</td>')
		htmlout.append('<td>'+drdroot.find('name').text+'</td><td>'+drdroot.get('type')+'</td><td>'+htmlruleEnabled+'</td><td>'+str(drdroot.find('notes').text)+'</td>')
		htmlout.append('<td>'+(''.join(htmlTestArray))+'</td>')
		htmlout.append('</tr>')
		print()
	print(' '.join(htmlout))


if __name__ == "__main__":
    main()
