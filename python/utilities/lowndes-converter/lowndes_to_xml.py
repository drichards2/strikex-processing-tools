from lowndes import lowndes
from lxml import etree


def loadlowndesfile(filename):
    lowndes_data = lowndes.read(filename)
    return lowndes_data


def createxml(lowndes_data, validate=True):
    transcription = etree.Element("transcription")
    NS = 'http://www.w3.org/2001/XMLSchema-instance'
    location_attribute = '{%s}schemaLocation' % NS
    transcription.set(location_attribute, 'http://drichards2.github.io/toast-visualiser/xsd/enhanced-strike-definition.xsd')

    dataSources = etree.SubElement(transcription, "dataSources")
    dataSource = etree.SubElement(dataSources, "dataSource")
    name = etree.SubElement(dataSource, "name")
    name.text = getname(lowndes_data)

    configParameters = etree.SubElement(dataSource, "configParameters")
    # TODO; Select parameters more carefully
    for key in lowndes_data["info"]:
        parameter = etree.SubElement(configParameters, "parameter")
        parameterName = etree.SubElement(parameter, "parameter")
        parameterName.text = key
        parameterValue = etree.SubElement(parameter, "value")
        parameterValue.text = str(lowndes_data["info"][key])

    strikeData = etree.SubElement(transcription, "strikeData")
    for strike in lowndes_data['strikedata'].iterrows():
        panda_frame = strike[1]
        strike = etree.SubElement(strikeData, "strike")
        bell = etree.SubElement(strike, "bell")
        bell.text = str(panda_frame['bell'])

        original = etree.SubElement(strike, "original", source=getname(lowndes_data))
        original.text = str(panda_frame['time'])

    tree = etree.ElementTree(transcription)
	
    if validate:
        print "Starting validation"
        xmlschema_doc = etree.parse("http://drichards2.github.io/toast-visualiser/xsd/enhanced-strike-definition.xsd")
        schema = etree.XMLSchema(xmlschema_doc)
        is_valid = schema.validate(tree)
        print "XML valid: {0}".format( is_valid )

    return tree


def savexml(tree, target_file):
    with open(target_file, 'w') as ostrm:
        ostrm.write( etree.tostring(tree, pretty_print=True) )


def getname(lowndes_data):
    return str.split(lowndes_data["info"]["creator"], " ")[0]


if __name__ == '__main__':
    stringName = 'exampleData_a.txt'
    data = loadlowndesfile(stringName)
    tree = createxml(data)
    savexml(tree, 'output.xml')