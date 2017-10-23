import unittest, sqlite3, sys
sys.path.append('/home/socall/projects/phosphorylation')

from controller.read_file import get_proteins_modifications_from_pd, add_proteins_to_db,\
    add_modifications_to_db

######################################################
#                                                    #
# Need to supply a database file - is this an issue? #
#                                                    #
######################################################

class TestReadFile(unittest.TestCase):
 
    def setUp(self):
        self.pdfile = 'test_pd_data.xlsx'
        #self.conn = sqlite3.connect('../model/phospho-db.sqlite') #Is this ok?
        #self.db_cursor = self.conn.cursor()
        self.proteins, self.modifications = get_proteins_modifications_from_pd(self.pdfile)
        
    def test_protein_modification_reading(self):
        self.assertEqual(self.proteins[0].get_uprotid(), 'Q9UKA4')
        self.assertEqual(self.modifications[2].get_position(), 323)
        self.assertEqual(self.proteins[0].get_uprotid(), \
                         self.modifications[0].get_protein())

    #def test_protein_database_update(self):
        #pass
        #add_proteins_to_db(self.proteins, self.db_cursor)
        ## code to grab last entry from db
        #self.assertEqual(self.proteins[-1].get_uprotid(), 'O43823')

    #def test_modifications_database_update(self):
        #pass
        #add_modifications_to_db(self.modifications, self.db_cursor)
        ## code to grab last entry from db
        #self.assertEqual(self.modifications[-1], 328)
        
        
 
if __name__ == '__main__':
    unittest.main()
