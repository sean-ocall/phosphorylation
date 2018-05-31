import urllib,urllib2
import xml.etree.ElementTree as ET

def get_AA_sequence_around_mod(residue, position, uniprotid):
    """
    Given a single uniprotid, a residue and the position of the phosphosite,
    return the amino acid sequence around the position. (from -8 to +7)
    """
    # This link returns a fasta file with the protein's sequence
    link = "http://www.uniprot.org/uniprot/" + uniprotid + ".fasta"
    f = urllib.urlopen(link)
    fasta = f.read()
    sequence = ''
    for part in fasta.split('\n')[1:]:
        sequence = sequence + part

    #Return sequence around phosphosite, 7 AAs before, the site, then 7AAs after
    if position < 8: # If the site is near to the start of the protein
        small_seq = sequence[:position+8]
        num_dashes = 15-len(small_seq)
        return_sequence =  num_dashes*"-" + small_seq 
    elif position > len(sequence)-7: # If it's near the end
        small_seq = sequence[position-8:]
        num_dashes = 15-len(small_seq)
        return_sequence = small_seq + num_dashes*"-"
    else: #It's in the middle
        return_sequence = sequence[position-8:position+7]

    new_return_sequence = ""
    for ch in return_sequence:
        if ch in ['S','T','Y']:
            new_return_sequence = new_return_sequence + ch.lower()
        else:
            new_return_sequence = new_return_sequence + ch

    return new_return_sequence




def put_genenames_in_db(db_cursor, email):
    """
    Translate the protein id to genename and add it to the main database
    """
    db_cursor.execute("SELECT uniprotid, genename FROM phosphositetb;")
    results = db_cursor.fetchall()
    #print results

    uniprotids = []
    uprotid_dict = {} # A little wasteful but solves a problem cleanly
    
    for uniprotid, genename in results:
        if genename == None:
            # Where uniprot id is e.g. A0FGR8-6
            # The '-6' part will cause conversion to genename to fail
            # So catch this and sort it out here
            if uniprotid[-2] == '-':
                #print "shortened %s to %s"%(uniprotid,uniprotid[:-2])
                full_uniprotid = uniprotid
                uniprotid = uniprotid[:-2]
            elif uniprotid[-3] == '-':
                full_uniprotid = uniprotid
                uniprotid = uniprotid[:-3]
            else:
                full_uniprotid = uniprotid
            uniprotids.append(uniprotid)
            # This dict will allow conversion back to full uniprotid
            uprotid_dict[uniprotid] = full_uniprotid
           

    uprot_to_genename_dict = get_genenames_from_uniprotids(uniprotids, email)

    for uprot, genename in uprot_to_genename_dict.iteritems():
        db_cursor.execute('UPDATE phosphositetb SET genename=? where uniprotid=?',
                          [genename,uprotid_dict[uprot]])


        
def get_genenames_from_uniprotids(uniprotids, email):
    """
    Use Uniprot API to find genenames given a list of uniprotids
    """
    url = 'http://www.uniprot.org/uploadlists/'

    str_all_uprots = ""
    for uprot in uniprotids:
        str_all_uprots = str_all_uprots +  uprot + " "
    
    params = {
    'from':'ACC',
    'to':'GENENAME',
    'format':'tab',
    'query':str_all_uprots
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = email 
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read(200000)

    lines = page.split('\n')
    print lines

    uprot_to_genename_dict = {}

    for line in lines[1:]:
        if line != "":
            #print "line", line
            parts = line.split('\t')
            #print "parts", parts
            #print parts
            uprot_to_genename_dict[parts[0]] = parts[1].strip('\n')

    return uprot_to_genename_dict




def put_function_in_db(db_cursor):
    """
    Look up the function description on Uniprot and add it to the proteintb in 
    the main database
    """
    db_cursor.execute("SELECT uniprotid, function FROM phosphositetb;")
    results = db_cursor.fetchall()

    completed_requests = []

    for uniprotid, function in results:
        if function is None and uniprotid not in completed_requests:
            url = "http://www.uniprot.org/uniprot/" + uniprotid + ".xml"
            url_content = urllib.urlopen(url)
            xml_content = url_content.read()
            
            root = ET.fromstring(xml_content)
            
            function = root.findall('.//{http://uniprot.org/uniprot}comment')
            for f in function:
                if f.attrib['type'] == 'function':
                    function_text = "<a href='"+ url.strip('.xml')  + "'>" +  "{}".format(f.find('.//{http://uniprot.org/uniprot}text').text) + "</a>"
                    db_cursor.execute('UPDATE phosphositetb SET function=? where uniprotid=?', (function_text, uniprotid))
                    print "put", function_text, ' in uniprotid:', uniprotid
            completed_requests.append(uniprotid)
