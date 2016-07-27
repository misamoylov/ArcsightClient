# -*- coding: utf8 -*-
import xmltodict

def get_xmlNameSpace(caseXml):
    """Get xml name spaces from case in XML format

            :param caseXml: case in XML format
            :type caseXml: string
            :return xmlNameSapce: XML name space
            :type xmlNameSpace: string

            """
    startIndex = caseXml.index("xmlns")
    endIndex = caseXml.index("><ns4:return>")
    xmlNameSpace = caseXml[startIndex:endIndex]
    return xmlNameSpace


def get_caseBodyXml(caseXml):
    """Get xml body from case in XML format

            :param caseXml: case in XML format
            :type caseXml: string
            :return caseBodyXml: body xml
            :type caseBodyXml: string

            """
    # extract case body
    startIndex = caseXml.index("<ns4:return>") + 12
    endIndex = caseXml.index("</ns4:return>")
    caseBodyXml = caseXml[startIndex:endIndex]
    # remove <referenceString>
    startIndex = caseBodyXml.index("<referenceString>")
    endIndex = caseBodyXml.index("</referenceString>") + 18
    caseBodyXml = caseBodyXml[0:startIndex] + caseBodyXml[endIndex:]
    return caseBodyXml


def get_updateXml(xmlNameSpace, authtoken, caseBodyXml):
    """Create XML for case updating.

            :param xmlNameSpace: XML name space
            :type xmlNameSpace: string
            :param authtoken: authentication token from Arcsight API
            :type authtoken: string
            :param caseBodyXml: XML body for updating
            :type caseBodyXml: string
            :return new XML string for updating case

            """
    caseUpdateXml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
    caseUpdateXml += "<ns4:update " + xmlNameSpace + ">";
    caseUpdateXml += "<ns4:authToken>" + authtoken + "</ns4:authToken>";
    caseUpdateXml += "<ns4:resource>" + caseBodyXml + "</ns4:resource>";
    caseUpdateXml += "</ns4:update>"
    return caseUpdateXml


def arcsight_case_field_change(caseBodyXml, fieldName, newValue):
    startIndex = caseBodyXml.index('<{}>'.format(fieldName)) + len('<{}>'.format(fieldName))
    endIndex = caseBodyXml.index('</{}>'.format(fieldName))
    oldValue = caseBodyXml[startIndex:endIndex]
    if oldValue == 0:
        caseBodyXml = caseBodyXml[:startIndex] + newValue + caseBodyXml[startIndex:]
    else:
        caseBodyXml = caseBodyXml.replace(oldValue, newValue)
    return caseBodyXml


def arcsight_case_field_add(caseBodyXml, fieldName, value):
    field = '<{}>'.format(fieldName) + value + '</{}>'.format(fieldName)
    caseBodyXml = caseBodyXml + field
    return caseBodyXml


def get_case_creation_time(caseXml):
    caseDict = xmltodict.parse(caseXml)
    return caseDict['ns4:getResourceByIdResponse']['ns4:return']['createdTimestamp']







