import urllib, urllib2
import xml.etree.ElementTree as ET

def get_function_from_uniprot(uniprotid):
    """
    Go to uniprot and find out if 'keyword' is one of the keywords
    for this accession number on uniprot
    """
    url = "http://www.uniprot.org/uniprot/" + uniprotid + ".xml"
    url_content = urllib.urlopen(url)
    xml_content = url_content.read()

    root = ET.fromstring(xml_content)

    function = root.findall('.//{http://uniprot.org/uniprot}comment')

    function_text = ''

    for f in function:
        if f.attrib['type'] == 'function':
            function_text = function_text + "{}".format(f.find('.//{http://uniprot.org/uniprot}text').text)

    return function_text

def get_keywords_from_uniprot(uniprotid):
    """
    Go to uniprot and find out if 'keyword' is one of the keywords
    for this accession number on uniprot
    """
    url = "http://www.uniprot.org/uniprot/" + uniprotid + ".xml"
    url_content = urllib.urlopen(url)
    xml_content = url_content.read()

    root = ET.fromstring(xml_content)

    keywords = root.findall('.//{http://uniprot.org/uniprot}keyword')
    return_list = [k.text for k in keywords]

    return return_list

def get_geneids_from_uniprot(uniprotids):

    str_all_uprots = ''

    url = 'http://www.uniprot.org/uploadlists/'

    for uprot in uniprotids:
        str_all_uprots = str_all_uprots + uprot + ' '

    params = {
    'from':'ACC',
    'to':'GENENAME',
    'format':'tab',
    'query':str_all_uprots
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = "spoc@unimelb.edu.au" 
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read(200000)

    lines = page.split('\n')

    uprot_to_genename_dict = {}

    for line in lines:
        if line != "":
            parts = line.split('\t')
            #print parts
            uprot_to_genename_dict[parts[0]] = parts[1].strip('\n')

    return uprot_to_genename_dict
