from xml.dom import minidom
scl = minidom.parse("D:\\Phyton61850\\test\\DataTypeTemplates.xml")
lNodeTypes = scl.getElementsByTagName("LNodeType")
for lNodeType in lNodeTypes:
    id = lNodeType.getAttribute("id")
    lnClass = lNodeType.getAttribute("lnClass")
    try:
        desc = lNodeType.getAttribute("desc")
    except:
        desc = ""
    print lnClass + ": " + id + " = " + desc