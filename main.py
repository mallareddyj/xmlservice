# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from xmlgenerator import XmlGenerator


def main(file_name):
    a = XmlGenerator()
    a.generate_xml(file_name)
    return


if __name__ == '__main__':
    filename = "/Users/mallareddy/Downloads/Facebook Jobs Feed - Dedicated West 3.9.2021 - Sheet1.csv"
    main(filename)
