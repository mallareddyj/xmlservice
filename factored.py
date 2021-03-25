
#! usr/bin/python
#
# -*- coding: utf-8 -*-
import csv, sys, os
from lxml import etree
from io import StringIO, BytesIO
import html
from unicodedata import normalize

def main():

	csvFile = 'Facebook Jobs Expedited Feed - 3.8.2021 - Sheet1.csv'
	csvData = csv.reader(open(csvFile,encoding = 'utf-8'), delimiter=',')

	header = next(csvData)
	csvData = list(csvData)

	root = etree.Element('jobs')
	# xmlFile = open('FacebookJobsExpeditedFeed382021first25k.xml', 'w')
	xmlFile = open('first.xml', 'w')
	xmlFile.write('<?xml version="1.0" encoding="UTF-8" ?> \n')

	for i in range(0,25000):
		row = csvData[i]
		products = etree.SubElement(root,'job')
		for index in range(0, len(header)):
			headLine = etree.SubElement(products, header[index])
			text = str(row[index])
			# text = str(text.encode('','ignore').decode())
			# text = text.replace("’","'")
			#nheadLine.text = html.unescape(text) # row[index]
			headLine.text = text
			headLine.text = "<![CDATA[ " + headLine.text + " ]]>"
			products.append(headLine)

	result = etree.tostring(root, pretty_print=True)
	result = result.decode()
	result = html.unescape(result)
	#bprint(result)
	xmlFile.write(result)

	root = etree.Element('jobs')
	# xmlFile = open('FacebookJobsExpeditedFeed382021first25k.xml', 'w')
	xmlFile = open('second.xml', 'w')
	xmlFile.write('<?xml version="1.0" encoding="UTF-8" ?> \n')

	for i in range(25000,50000):
		row = csvData[i]
		products = etree.SubElement(root,'job')
		for index in range(0, len(header)):
			headLine = etree.SubElement(products, header[index])
			text = str(row[index])
			# text = str(text.encode('utf-8','ignore').decode())
			text = text.replace("’","'")
			headLine.text = html.unescape(text) # row[index]
			headLine.text = "<![CDATA[ " + headLine.text + " ]]>"
			products.append(headLine)

	result = etree.tostring(root, pretty_print=True)
	result = result.decode()
	result = html.unescape(result)
	#bprint(result)
	xmlFile.write(result)

	root = etree.Element('jobs')
	# xmlFile = open('FacebookJobsExpeditedFeed382021first25k.xml', 'w')
	xmlFile = open('third.xml', 'w')
	xmlFile.write('<?xml version="1.0" encoding="UTF-8" ?> \n')

	for i in range(50000,len(csvData)):
		row = csvData[i]
		products = etree.SubElement(root,'job')
		for index in range(0, len(header)):
			headLine = etree.SubElement(products, header[index])
			text = str(row[index])
			# text = str(text.encode('utf-8','ignore').decode())
			text = text.replace("’","'")
			headLine.text = html.unescape(text) # row[index]
			headLine.text = "<![CDATA[ " + headLine.text + " ]]>"
			products.append(headLine)

	result = etree.tostring(root, pretty_print=True)
	result = result.decode()
	result = html.unescape(result)
	#bprint(result)
	xmlFile.write(result)


if __name__ == '__main__':
	main()