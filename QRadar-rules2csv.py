# python3 script
import sys, os
import json, time
from xml.etree.ElementTree import ElementTree
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
	htmlout=[]

	global testSeq

	for rule in root.findall('custom_rule'):
		fullTestArray=[]
		htmlTestArray=[]
		htmlRuleDef=[]
		parser = MyHTMLParser()
		htmlGroupArray=[]

		ruleUUID=rule.find('uuid').text
		ruleID=rule.find('id').text
		fgroupGet="fgroup_link[id='"+ruleID+"']"
		fgroupGet="fgroup_link"

		ruleOrigin=rule.find('origin').text


		for fgroup_link in root.findall('fgroup_link[item_id="'+ruleID+'"]'):
			if fgroup_link is None: print('Error')

			fgroup_link_fgroup_id = fgroup_link.find('fgroup_id').text
			fgroup_id             = root.find('fgroup[id="'+fgroup_link_fgroup_id+'"]')
			fgroup_name           = fgroup_id.find('description').text
			fgroup_parent_id      = fgroup_id.find('parent_id')
			fgroup_level_id=0
			fgroup_level_id       = fgroup_id.find('level_id').text
			level=">"
			
			htmlGroupArray.append('"'+level+str(fgroup_name)+'"')
			while not fgroup_parent_id is None:
				fgroup_id       = root.find('fgroup[id="'+fgroup_parent_id.text+'"]') #find parent node
				fgroup_name     = fgroup_id.find('description').text #find name
				fgroup_level_id=0
				fgroup_level_id = fgroup_id.find('level_id').text
				level=level+">"
				fgroup_parent_id=fgroup_id.find('parent_id') #check if new node has parent

				if not fgroup_parent_id is None:
					htmlGroupArray.append('"'+level+str(fgroup_name)+'"')

		detailedRuleData=base64.b64decode(rule.find('rule_data').text)
		x = etree.fromstring(detailedRuleData)
		m = etree.tostring(x, pretty_print = True)

		drdroot = ET.fromstring(detailedRuleData)

		ruleName=drdroot.find('name').text
		ruleType=drdroot.get('type')
		htmlRuleDef.append('"'+ruleName+'"')

		htmlRuleDef.append('"'+ruleOrigin+'"')
		htmlRuleDef.append('"'+ruleType+'"')
	
		ruleIsBB=drdroot.get('buildingBlock')
		if ruleIsBB is not None and ruleIsBB=='true':
			htmlRuleDef.append('"BB"')
		else:
			htmlRuleDef.append('"Rule"')

		ruleEnabled=drdroot.get('enabled')
		if ruleEnabled=='true':
			htmlruleEnabled='"Enabled"'
		else:
			htmlruleEnabled='"Disabled"'

		htmlRuleDef.append(htmlruleEnabled)
		htmlRuleDef.append('"'+ruleUUID+'"')


# start of ruletest definition
		testDefinitions=drdroot.find('testDefinitions')

		negateTextA=''
		negateTextA=' [AND NOT] '
		negateTextB=''
		testSeq=-1
		htmlTestArray=['"']
		for elTests in testDefinitions.findall('test'):
			teteststSeq=testSeq+1
			testName=elTests.get('name')
			testUUID=elTests.get('uid')
			testNegate=str(elTests.get('negate'))
			ruleText=str(elTests.find('text').text)
			htmltest=''
			if testNegate=="true" and testNegate is not None:
				htmltest=''+negateTextA+''
			else:
				htmltest=''+negateTextB+''

			negateTextA=' [AND NOT] '
			negateTextB=' [AND] '

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
						htmltest=''+htmltest+''
				htmltest=htmltest+''+str(x[2])+''
			
			htmlTestArray.append(htmltest)
		htmlTestArray.append('"')

		actionDefinitions=drdroot.find('actions')
		responsDefinitions=drdroot.find('responses')
		responsHTML=[]

		forceOffense='false'

		if responsDefinitions is not None:
			newevent=responsDefinitions.find('newevent')
			if newevent is not None:
				neweventqid = str(newevent.get('qid'))
				LLC=str('LLC:'+str(newevent.get('lowLevelCategory')))
				CRS=str('CRS:'+str(newevent.get('credibility'))+str(newevent.get('relevance'))+str(newevent.get('severity')))
				forceOffense=str(newevent.get('forceOffenseCreation'))
				if forceOffense is not None and forceOffense=='true':
					htmlforceOffense='Offense'
				else:
					htmlforceOffense='No-Offense'

				responsHTML.append(str('"QID:'+str(newevent.get('qid')))+'","'+htmlforceOffense+'","'+LLC+'","'+CRS+'"')
		else:
			responsHTML.append(str('"","","",""'))
	
		print(','.join(htmlRuleDef)+','+','.join(htmlTestArray)+','+','.join(responsHTML)+','+','.join(htmlGroupArray))

	print('END')


if __name__ == "__main__":
    main()
    
