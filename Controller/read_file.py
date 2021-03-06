import sqlite3, argparse, numpy
import pandas as pd
from Class import Phosphosite
from uniprot_tools import  put_genenames_in_db, put_function_in_db, get_AA_sequence_around_mod,get_genenames_from_uniprotids 

help_msg = "Adds data from Proteome Discoverer output to given DB"
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument('--databasefile', help='sqlite3 file (or blank)')
parser.add_argument('--pdfile', help='Proteome Discoverer Output')
parser.add_argument('--email', default='spoc@unimelb.edu.au', help='Email address required for using Uniprot API for certain lookup features')



def get_phosphosites_from_pd(pdfile):
    """
    Read a Proteome Discoverer output file and extract Phosphosite
    objects from it. Return them as a list
    """
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
    phosphosites = []

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

        for i, resid in enumerate(inner_aacids):
            new_psite = Phosphosite(resid, inner_pos[i], uprot_name, avg)
            phosphosites.append(new_psite)

    return phosphosites

def add_AA_sequences_to_db(db_cursor):
    """
    Add the amino acid sequence around the phosphosite to the phosphositetb in
    the main database
    """
    db_cursor.execute("SELECT rowid,residue,position,uniprotid FROM phosphositetb")
    results = db_cursor.fetchall()
    #print results

    for rowid, residue, position, uniprotid in results:
        AA_sequence = get_AA_sequence_around_mod(residue,position,uniprotid)
        #print AA_sequence
        #db_cursor.execute("SELECT rowid, AA_sequence FROM  phosphositetb")
        #print db_cursor.fetchall()
        db_cursor.execute("UPDATE phosphositetb SET AA_sequence=? where rowid=?;"\
                              ,(AA_sequence,rowid))

def add_phosphosites_to_db(phosphosites, db_cursor):
    """
    Extract info from Phosphosite objects and add to phosphositetb in main
    database
    """

    for phosphosite in phosphosites:
        residue = phosphosite.get_residue()
        position = phosphosite.get_position()
        uniprotid = phosphosite.get_uniprotid()
        fold_change = phosphosite.get_fold_change()
        db_cursor.execute(\
                          "INSERT INTO phosphositetb (residue,position,uniprotid,foldchange) VALUES(?,?,?,?);"\
                          ,(residue,position,uniprotid,fold_change))
        
if __name__ == "__main__":
    args = parser.parse_args()

    conn = sqlite3.connect(args.databasefile)
    db_cursor = conn.cursor()

    phosphosites = get_phosphosites_from_pd(args.pdfile)

    add_phosphosites_to_db(phosphosites, db_cursor)
    put_genenames_in_db(db_cursor, args.email)
    #put_function_in_db(db_cursor)
    add_AA_sequences_to_db(db_cursor)

    #######################################################################################
    #
    # For testing purposes:
    #
    #######################################################################################
    db_cursor.execute('SELECT rowid, AA_sequence, uniprotid, genename FROM phosphositetb;')
    print "Rowid\tUNIPROT Genename"
    for rowid,AA_sequence,uniprotid,genename in db_cursor.fetchall():
        print rowid,"\t",AA_sequence,"\t",uniprotid,"  ",genename

    conn.commit() # might be better to do this in the functions?? would have to pass conn instead of cursor
    conn.close()
