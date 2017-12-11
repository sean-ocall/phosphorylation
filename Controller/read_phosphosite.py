import sys
import pandas as pd
from Class import Phosphosite

def get_phosphosites_from_file(phosphositefile):
    """
    Read a phosphosite kinase substrate file and put the contents into 
    Phosphosite objects
    """
    csv = pd.read_csv(phosphositefile, sep='\t', skiprows=3)
    print csv.head()
    
    kinases = csv["KINASE"]
    kin_acc_ids = csv["KIN_ACC_ID"]
    kinase_organisms = csv["KIN_ORGANISM"]
    substrates = csv['SUBSTRATE']
    sub_acc_ids = csv['SUB_ACC_ID']
    substrate_organisms = csv["SUB_ORGANISM"]
    sites_residues = csv['SUB_MOD_RSD']
    AA_sequences = csv["""SITE_+/-7_AA"""]

    phosphosites = []

    for i,substrate in enumerate(substrates):
        # Are we interested in all species?
        #if kinase_organisms[i] == 'human' and substrate_organisms[i] == 'human':
        residue = sites_residues[i][0]
        site = int(sites_residues[i][1:])
        new_phosphosite = Phosphosite(substrate, sub_acc_ids[i], kinases[i], \
                                          kin_acc_ids[i], site,residue, AA_sequences[i])
        phosphosites.append(new_phosphosite)

    return phosphosites

if __name__=="__main__":
    phosphosites = get_phosphosites_from_file(sys.argv[1])
    print "substrate:\tkinase"
    print phosphosites[10].get_substrate(),":\t",phosphosites[10].get_kinase()
    print phosphosites[10].get_AA_sequence()
    
