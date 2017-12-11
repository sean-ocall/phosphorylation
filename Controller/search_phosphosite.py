"""
Read the phosphosite Kinase_substrate_data file, compare to 
sites found by pd in our custom database, and try to find clusters
of substrates with the same kinase in our data

usage: python search_phosphosite.py [database_file] [phosphosite_file]
"""
import sqlite3, sys
from read_phosphosite import get_phosphosites_from_file

def compare_phosphosites_strict(modtb_result, phosphosites):

    found_phosphosites = []

    for modtb_result in modtb_results:
    
        modid = modtb_result[0]
        residue = modtb_result[1]
        position = modtb_result[2]
        uniprotid = modtb_result[3]

        for psite in phosphosites:
            if residue == psite.get_residue() and\
               position == psite.get_position() and\
               uniprotid == psite.get_sub_acc_id():
                found_phosphosites.append(psite)
                
    return found_phosphosites

def compare_phosphosites_residue_only(modtb_result, phosphosites):
    found_phosphosites = []
    found_modtb_results = []
    
    for modtb_result in modtb_results:
    
        modid = modtb_result[0]
        residue = modtb_result[1]
        position = modtb_result[2]
        uniprotid = modtb_result[3]

        for psite in phosphosites:
            if residue == psite.get_residue() and\
               uniprotid == psite.get_sub_acc_id():
                found_phosphosites.append(psite)
                found_modtb_results.append(modtb_result)
                
    return found_phosphosites, found_modtb_results    

def compare_phosphosites_relaxed(modtb_result, phosphosites):
    found_phosphosites = []
    found_modtb_results = []

    for modtb_result in modtb_results:
    
        modid = modtb_result[0]
        residue = modtb_result[1]
        position = modtb_result[2]
        uniprotid = modtb_result[3]

        for psite in phosphosites:
            if uniprotid == psite.get_sub_acc_id():
                found_phosphosites.append(psite)
                found_modtb_results.append(modtb_result)
                
    return found_phosphosites, found_modtb_results

if __name__=="__main__":

    conn = sqlite3.connect(sys.argv[1])
    db_cursor = conn.cursor()

    db_cursor.execute("SELECT modid,residue,position,proteinid,AA_sequence FROM modificationtb")
    modtb_results = db_cursor.fetchall()

    phosphosites = get_phosphosites_from_file(sys.argv[2])

    matches_strict = compare_phosphosites_strict(modtb_results, phosphosites)
    matches_relaxed, found_modtbs = compare_phosphosites_residue_only(modtb_results, phosphosites)

    print "Matches for substrate only"
    print "Kinase\tSubstrate\tFound Postition\tAndyPosition"
    for i, match in enumerate(matches_relaxed):
        print match.get_kinase(), "\t", match.get_substrate(), "\t", match.get_residue(), match.get_position(), "\t", found_modtbs[i][1], found_modtbs[i][2]
        print match.get_AA_sequence()
        print found_modtbs[i][4]
        

    print ""
    print ""
    print "Kinase\tSubstrate"
    for match in matches_strict:
        print match.get_kinase(), ":\t", match.get_substrate()

    
