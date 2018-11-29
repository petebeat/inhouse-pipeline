import xml.etree.ElementTree as ET

def getCCCID(cccFile):
    '''
    ccc files need to have the cccid set to work. We will grab it from the file
    manually. only grabs the first element's cccid
    '''
    try:
        tree = ET.parse(cccFile)
        root = tree.getroot()
        return root[0].attrib['id']
    except:
        return ''
