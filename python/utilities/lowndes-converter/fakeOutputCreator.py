from lxml import etree
import lowndes_to_xml
import random


def loadxmlfile(filename):
    tree = etree.parse(filename)
    return tree


def addfakeoutput(tree):
    strikes = tree.findall(".//strike")

    for strike in strikes:
        if float(strike.find("original").text) > 61670:
            modelOutput = etree.SubElement(strike, "modelOutput", source="RodModel2")
            time = etree.SubElement(modelOutput, "time")
            time.text = str(float(strike.find("original").text)*(1 + 0.05*(-0.5+random.random())))
            print etree.tostring(strike, pretty_print=True)
        else:
            strike.find('..').remove(strike)
    return tree

if __name__ == '__main__':
    originalData = loadxmlfile('exampleData_a.xml')

    processedtree = addfakeoutput(originalData)

    outputFileName = 'modelData_a.xml'
    lowndes_to_xml.savexml(processedtree, outputFileName)
