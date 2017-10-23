import sqlite3, argparse
import pandas as pd
import numpy
from Class import Protein, Modification

help_msg = "Adds data from Proteome Discoverer output to given DB"
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument('databasefile', help='sqlite3 file (or blank)')
parser.add_argument('pdfile', help='Proteome Discoverer Output')


        
def add_proteins_to_db(proteins, db_cursor, get_inserted_ids=False):
    existing_proteins = db_cursor.execute("SELECT uniprotid FROM proteintb")
    inserted_ids = []
    for protein in proteins:
        up_id = protein.get_uprotid()
        if up_id not in existing_proteins:
            db_cursor.execute("INSERT INTO proteintb (uniprotid) VALUES(?);"\
                              ,(up_id,))
            inserted_ids.append(db_cursor.lastrowid)

    if get_inserted_ids:
        return inserted_ids

def add_modifications_to_db(modifications,db_cursor, get_inserted_ids=False):
    inserted_ids = []
    for modification in modifications:
        residue = modification.get_residue()
        position = modification.get_position()
        proteinid = modification.get_protein()
        db_cursor.execute("INSERT INTO modificationtb (residue,position,proteinid) VALUES(?,?,?);"\
                              ,(residue,position,proteinid))
        inserted_ids.append(db_cursor.lastrowid)

    if get_inserted_ids:
        return inserted_ids
    

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

    
