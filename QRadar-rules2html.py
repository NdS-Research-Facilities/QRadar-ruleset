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
enabled.red { \
        color: #bc232a;\
	font-weight: bold;\
      }\
enabled.green { \
        color: #749a56;\
	font-weight: bold;\
      }\
\
andnot.red { \
        color: #1606ed;\
	font-weight: bold;\
      }\
andnot.green { \
        color: #749a56;\
	font-weight: bold;\
      }\
\
offense.yes { \
        color: #bc232a;\
	font-weight: bold;\
      }\
offense.no { \
        color: #749a56;\
	font-weight: bold;\
      }\
\
BB.blue { \
        color: #1606ed;\
	font-weight: bold;\
      }\
BB.orange { \
        color: #ed7306;\
	font-weight: bold;\
      }\
\
Org.SYSTEM { \
        color: #749a56;\
	font-weight: bold;\
      }\
Org.OVERRIDE { \
        color: #bc232a;\
	font-weight: bold;\
      }\
Org.USER { \
        color: #ed7306;\
	font-weight: bold;\
      }\
\
Type.EVENT { \
        color: #749ad8;\
	font-weight: bold;\
      }\
Type.FLOW { \
        color: #749ad8;\
	font-weight: bold;\
      }\
Type.COMMON { \
        color: #749a56;\
	font-weight: bold;\
      }\
Type.OFFENSE { \
        color: #ed7306;\
	font-weight: bold;\
      }\
Type.ANOMALY {\
        color: #ed7306;\
	font-weight: light;\
      }\
tree.dm {\
        color: #400000;\
	font-size: 7px;\
      }\
\
</style>\
\
<table class="sample">\
    <tr>\
        <th width="33%">Name</th>\
        <th  width="33%">Rule</th>\
        <th  width="33%">Respons</th>\
    </tr>\
\
\
']

	global testSeq

	for rule in root.findall('custom_rule'):
		fullTestArray=[]
		htmlTestArray=[]
		htmlRuleDef=[]
		parser = MyHTMLParser()

		ruleUUID=rule.find('uuid').text
		ruleID=rule.find('id').text
		fgroupGet="fgroup_link[id='"+ruleID+"']"
		fgroupGet="fgroup_link"

		ruleOrigin=rule.find('origin').text

		for fgroup_link in root.findall('fgroup_link[item_id="'+ruleID+'"]'):
			if fgroup_link is None: print('Error')
			htmlGroupArray=[]
			fgroup_link_fgroup_id = fgroup_link.find('fgroup_id').text
			fgroup_id             = root.find('fgroup[id="'+fgroup_link_fgroup_id+'"]')
			fgroup_name           = fgroup_id.find('description').text
			fgroup_parent_id      = fgroup_id.find('parent_id')
			fgroup_level_id=0
			fgroup_level_id       = fgroup_id.find('level_id').text
			level=">"
#			print('  '+ruleID+' '+str(fgroup_name))
#			htmlGroupArray.insert(0,level+str(fgroup_name))
			
			htmlGroupArray.append('<tree class="dm">'+level+str(fgroup_name)+' </tree>')
			while not fgroup_parent_id is None:
				fgroup_id       = root.find('fgroup[id="'+fgroup_parent_id.text+'"]') #find parent node
				fgroup_name     = fgroup_id.find('description').text #find name
				fgroup_level_id=0
				fgroup_level_id = fgroup_id.find('level_id').text
				level=level+">"
				fgroup_parent_id=fgroup_id.find('parent_id') #check if new node has parent
#				print('> '+ruleID+' '+str(fgroup_name))
				if not fgroup_parent_id is None:
					htmlGroupArray.append('<tree class="dm">'+level+str(fgroup_name)+' </tree>')
#					htmlGroupArray.append(level+str(fgroup_name))
#				htmlGroupArray.insert(0,'>'+str(fgroup_name))
#		print('/'.join(htmlGroupArray))

		detailedRuleData=base64.b64decode(rule.find('rule_data').text)
		x = etree.fromstring(detailedRuleData)
		m = etree.tostring(x, pretty_print = True)

		drdroot = ET.fromstring(detailedRuleData)

		ruleName=drdroot.find('name').text
		ruleType=drdroot.get('type')
		htmlRuleDef.append(ruleName)
		htmlRuleDef.append('<br>')

		htmlRuleDef.append('<Org class="'+ruleOrigin+'">'+ruleOrigin+' </Org>')
		htmlRuleDef.append('<Type class="'+ruleType+'">'+ruleType+' </Type>')
	
		ruleIsBB=drdroot.get('buildingBlock')
		if ruleIsBB is not None and ruleIsBB=='true':
			htmlRuleDef.append('<BB class="blue">BuildingBlock </BB>')
		else:
			htmlRuleDef.append('<BB class="orange">Rule </BB>')

		ruleEnabled=drdroot.get('enabled')
		if ruleEnabled=='true':
			htmlruleEnabled='<enabled class="green">Enabled</enabled>'
		else:
			htmlruleEnabled='<enabled class="red">Disabled</enabled>'

		htmlRuleDef.append(htmlruleEnabled)
		htmlRuleDef.append('<br>')

		htmlRuleDef.append('<br>'.join(htmlGroupArray))
		htmlRuleDef.append('<br>')

		htmlRuleDef.append(ruleUUID)
		htmlRuleDef.append('<br>')

# start of ruletest definition
		testDefinitions=drdroot.find('testDefinitions')

		negateTextA=''
		negateTextA=' AND NOT '
		negateTextB=''
		testSeq=-1
		for elTests in testDefinitions.findall('test'):
			teteststSeq=testSeq+1
			testName=elTests.get('name')
			testUUID=elTests.get('uid')
			testNegate=str(elTests.get('negate'))
			ruleText=str(elTests.find('text').text)
			htmltest=''
			if testNegate=="true" and testNegate is not None:
				htmltest='<andnot class="red">'+negateTextA+'</andnot>'
			else:
				htmltest='<andnot class="red">'+negateTextB+'</andnot>'

			negateTextA=' AND NOT '
			negateTextB=' AND '

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
				htmltest=htmltest+str(x[2])+'</b>'
			
			htmlTestArray.append(htmltest)
#		actionDefinitions=['']
#		responsDefinitions=[]
#		actionDefs=ElementTree().getroot()
#		responsDefs=[]
#		stub=ElementTree().getroot()

		actionDefinitions=drdroot.find('actions')
		responsDefinitions=drdroot.find('responses')
		responsHTML=''
#		if actionDefinitions is not None: responsHTML=responsHTML+str(actionDefinitions.items())

		forceOffense='false'

		if actionDefinitions is not None:
			for actions in actionDefinitions:
				S1='';S2='';S3=''
				if actions is not None:
					if actions.get('value') is not None: S3=actions.get('value')
					if actions.get('operation') is not None: S2=actions.get('operation')[3];S1=actions.get('operation')[0]
					if S1=='s': S1='='
					if S1=='i': S1='+'
					if S1=='d': S1='-'
					
				responsHTML=responsHTML+str(S2+S3+S1)+'<br>'

		if responsDefinitions is not None:
			responsHTML=responsHTML+str(responsDefinitions.items())+'<br>'
			newevent=responsDefinitions.find('newevent')
			if newevent is not None:
				htmlGroupArray=[]
				fgroup_link_fgroup_id = fgroup_link.find('fgroup_id').text
				fgroup_id             = root.find('fgroup[id="'+fgroup_link_fgroup_id+'"]')
				fgroup_name           = fgroup_id.find('description').text
				fgroup_parent_id      = fgroup_id.find('parent_id')
				fgroup_level_id=0
				fgroup_level_id       = fgroup_id.find('level_id').text
				level=">"
				neweventqid = str(newevent.get('qid'))
				fgroup_id   = root.find('fgroup[qid="'+fgroup_link_fgroup_id+'"]')
				


				responsHTML=responsHTML+str('QID: '+str(newevent.get('qid')))+' <br>'


				LLC=str('LLC : '+str(newevent.get('lowLevelCategory')))
				CRS=str('CRS : '+str(newevent.get('credibility'))+str(newevent.get('relevance'))+str(newevent.get('severity')))
				forceOffense=str(newevent.get('forceOffenseCreation'))
				if forceOffense is not None and forceOffense=='true':
					htmlforceOffense='<offense class="yes">Offense </enabled>'
				else:
					htmlforceOffense='<offense class="no">No-Offense </enabled>'


				responsHTML=responsHTML+htmlforceOffense+'<br>'
				responsHTML=responsHTML+LLC+'<br>'
				responsHTML=responsHTML+CRS+'<br>'

#				print(qid.get('qid'))
#				print(qid.get('lowLevelCategory'))
#				print(qid.get('forceOffenseCreation'))


##			for action in responsDefinitions.iter():
##				if action.tag is not None:

#					print(action.tag)
#					print(action.items())				
##					responsHTML=responsHTML+str(action.items())+'X'


#		print(actionHTML)
#		print(responsHTML)

#		actionDefs=[actionDefinitions,ET.Element('')][actionDefinitions is not None]
#		responsDefs=[responsDefinitions,ET.Element('empty')][responsDefinitions is not None]
#		print(responsDefs)
#		if responsDefs is not None:
#			for action in responsDefs.iter():
#				print(action.items())
		
#		print(actionDefs)


		#print(prtTestArray)
		#print(fullTestArray)
######		htmlout.append('<td>'+drdroot.find('name').text+'</td><td>'+ruleUUID+'</td><td>'+drdroot.get('type')+'</td><td>'+htmlruleEnabled+'</td><td>'+str(drdroot.find('notes').text)+'</td>')
	
		htmlout.append('<tr>')
		htmlout.append('<td>'+(''.join(htmlRuleDef))+'</td>')
#		htmlout.append('<td>'+str(ruleUUID)+'<p>isBB: '+str(ruleIsBB)+'<p>'+htmlruleEnabled+'<p>Type: '+drdroot.get('type')+'</td><td>'+drdroot.find('name').text+'</td><td>'+str(drdroot.find('notes').text)+'</td>')
		htmlout.append('<td>'+(''.join(htmlTestArray))+'</td>')
		htmlout.append('<td>'+(''.join(responsHTML))+'</td>')
#		htmlout.append('<td>'+responsHTML+'</td>')		
		htmlout.append('</tr>')
		print()
	print(' '.join(htmlout))


if __name__ == "__main__":
    main()
