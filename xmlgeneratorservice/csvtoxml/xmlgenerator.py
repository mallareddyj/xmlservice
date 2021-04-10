from lxml import etree
import html
from extractorfactory import factory
from constants import MAX_LIMIT


class XmlGenerator:
    def __init__(self):
        self.filename = ""
        self.csv_data = []

    def __generate_xml_interval(self, start, end):
        
        csv_data = self.csv_data
        header = csv_data[0]
        root = etree.Element('jobs')
        output_file = "/tmp/test.xml"
        xml_file = open(output_file, 'w')
        xml_file.write('<?xml version="1.0" encoding="UTF-8" ?> \n')
        for i in range(start, end):
            row = csv_data[i]
            node = etree.SubElement(root, 'job')
            for index in range(0, len(header)):
                head_line = etree.SubElement(node, header[index])
                text = str(row[index])
                head_line.text = "<![CDATA[ " + text + " ]]>"
                node.append(head_line)

        result = etree.tostring(root, pretty_print=True)
        result = result.decode()
        result = html.unescape(result)
        xml_file.write(result)
        return output_file

    def generate_xml(self, filename):

        self.filename = filename
        ending = filename.split(".")[-1]
        extractor = factory(ending)
        csv_data = extractor.extract_data(filename)
        self.csv_data = csv_data
        start = 1
        # output_files = []
        # for i in range(MAX_LIMIT+1, len(csv_data), MAX_LIMIT):
        #     end = i
        #     output_file = self.__generate_xml_interval(start, end)
        #     output_files.append(output_file)
        #     start = end

        output_file = self.__generate_xml_interval(start, len(csv_data))
        return output_file
        # output_files.append(output_file)
        # return output_files
