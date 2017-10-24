import sqlite3, argparse
import pandas as pd
import numpy
from Class import Protein, Modification
import urllib,urllib2



help_msg = "Adds data from Proteome Discoverer output to given DB"
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument('--databasefile', help='sqlite3 file (or blank)')
parser.add_argument('--pdfile', help='Proteome Discoverer Output')
parser.add_argument('--email', default='spoc@unimelb.edu.au')


        
def add_proteins_to_db(proteins, db_cursor):
    # Not sure monitoring for existing proteins is neccessary
    # Will probably end up with a single db for each PD file
    existing_proteins_cursor = db_cursor.execute("SELECT uniprotid FROM proteintb")
    existing_proteins = existing_proteins_cursor.fetchall()
    print "existing", existing_proteins
    existing_proteins_list = [i[0] for i in existing_proteins]
    print "as list:", existing_proteins_list

    for protein in proteins:
        up_id = protein.get_uprotid()
        if up_id not in existing_proteins_list:
            db_cursor.execute("INSERT INTO proteintb (uniprotid) VALUES(?);"\
                              ,(up_id,))

def put_genenames_in_db(db_cursor, email):
    db_cursor.execute("SELECT uniprotid, genename FROM proteintb;")
    results = db_cursor.fetchall()

    uniprotids = []
    
    for uniprotid, genename in results:
        if genename == None:
            uniprotids.append(uniprotid)

    uprot_to_genename_dict = get_genenames_from_uniprotids(uniprotids, email)
    
    for uprot, genename in uprot_to_genename_dict.iteritems():
        db_cursor.execute('UPDATE proteintb SET genename=? where uniprotid=?',
                          [genename,uprot])


        

def get_genenames_from_uniprotids(uniprotids, email):
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




def add_modifications_to_db(modifications,db_cursor, get_inserted_ids=False):

    for modification in modifications:
        residue = modification.get_residue()
        position = modification.get_position()
        proteinid = modification.get_protein()
        db_cursor.execute("INSERT INTO modificationtb (residue,position,proteinid) VALUES(?,?,?);"\
                              ,(residue,position,proteinid))



        

def get_proteins_modifications_from_pd(pdfile):
    xl = pd.ExcelFile(pdfile)
    sheetnames = xl.sheet_names

    df = xl.parse(sheetnames[0])

    mod_mast_prot = df.loc[:,"Modifications in Master Proteins"]
    df_fold_changes = df.loc[:,"Abundance Ratio: (Induce) / (Non Ind)"]

    remove_list = []
    for i, mod in enumerate(mod_mast_prot):
        if not isinstance(mod, basestring):
            remove_list.append(i)
        
    for i, change in enumerate(df_fold_changes):
        if numpy.isnan(change):
            if i not in remove_list:
                remove_list.append(i)

    for remove in remove_list:
        del mod_mast_prot[remove]
        del df_fold_changes[remove]

    fold_changes =  df_fold_changes.tolist()
    proteins = []
    modifications = []

    for i,prot in enumerate(mod_mast_prot):
        prot_mods = prot.split(' ', 1)
        uprot_name = prot_mods[0]
        mods = prot_mods[1]
        try:
            avg = fold_changes[i]
        except(KeyError):
            print "Key: ", i, "not found"

        parts = mods.split(']')
        for part in parts:
            if 'Phospho' in part:
                xpos = part.find('xP')
                num_phospos = int(part[xpos-1:xpos]) # " 1" in above example
                start_sq_bracs = part.find('[')
                phospho_data = part[start_sq_bracs+1:].split(' ')

                inner_aacids = []
                inner_pos = []

                for pho in phospho_data:
                    if '/' not in pho and '(' in pho: # Can have "T/S"
                        inner_aacids.append(pho[0])
                        start_round_brac = pho.find('(')
                        try:
                            inner_pos.append(int(pho[1:start_round_brac]))
                        except:
                            inner_pos.append(0) #sometimes not present in record
                    elif '/' not in pho and '(' not in pho:# often no (99.9) etc
                        inner_aacids.append(pho[0])
                        try:
                            inner_pos.append(int(pho.strip(';')[1:]))
                        except:
                            inner_pos.append(0) #sometimes not present in record

        new_protein = Protein(uprot_name)
        proteins.append(new_protein)
        for i, aacid in enumerate(inner_aacids):
            new_mod = Modification(aacid, inner_pos[i], uprot_name)
            modifications.append(new_mod)
    ##################################################################
    #                                                                # 
    # NB: we are grabbing the fold change, but doing nothing with it #
    #                                                                #
    ##################################################################
    return proteins, modifications
                        
    
if __name__ == "__main__":
    args = parser.parse_args()

    conn = sqlite3.connect(args.databasefile)
    db_cursor = conn.cursor()

    proteins, modifications = get_proteins_modifications_from_pd(args.pdfile)

    add_proteins_to_db(proteins, db_cursor)
    add_modifications_to_db(modifications, db_cursor)
    put_genenames_in_db(db_cursor, args.email)
    #db_cursor.execute('SELECT proteinid, uniprotid FROM proteintb;')
    #print db_cursor.fetchall()

    conn.commit() # might be better to do this in the functions?? would have to pass conn instead of cursor
    conn.close()

    
