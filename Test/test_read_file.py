"""
Unittests for Controller/read_file.py

Run from main project directory with: python -m unittest Test.test_read_file
"""
import unittest, sqlite3
from Controller.read_file import get_proteins_modifications_from_pd, add_proteins_to_db,\
    add_modifications_to_db


######################################################
#                                                    #
# Need to supply a database file - is this an issue? #
#                                                    #
######################################################

class TestReadFile(unittest.TestCase):
 
    def setUp(self):
        self.pdfile = 'Test/test_pd_data.xlsx'
        self.conn = sqlite3.connect('Model/phospho-db.sqlite') 
        self.db_cursor = self.conn.cursor()
        self.proteins, self.modifications = get_proteins_modifications_from_pd(self.pdfile)
        
        
    def test_protein_modification_reading(self):
        self.assertEqual(self.proteins[0].get_uprotid(), 'Q9UKA4')
        self.assertEqual(self.modifications[2].get_position(), 323)
        self.assertEqual(self.proteins[0].get_uprotid(), \
                         self.modifications[0].get_protein())

    def test_protein_database_update(self):
        inserted_ids = add_proteins_to_db(self.proteins, self.db_cursor, True)
        
        # code to grab last entry from db
        self.db_cursor.execute("SELECT uniprotid FROM proteintb ORDER BY proteinid DESC LIMIT 1;")
        result = self.db_cursor.fetchall()
        self.assertEqual(self.proteins[-1].get_uprotid(), result[-1][0])
        for ins_id in inserted_ids:
            # I believe that proteinid is equivalent to rowid because it's a primary key
            self.db_cursor.execute("DELETE FROM proteintb WHERE proteinid=?", (ins_id,))

    def test_modifications_database_update(self):
        inserted_ids = add_modifications_to_db(self.modifications, self.db_cursor, True)
        
        # code to grab last entry from db
        self.db_cursor.execute("SELECT position FROM modificationtb ORDER BY modid DESC LIMIT 1;")
        result = self.db_cursor.fetchall()
        self.assertEqual(self.modifications[-1].get_position(), result[-1][0])
        for ins_id in inserted_ids:
            # I believe that proteinid is equivalent to rowid because it's a primary key
            self.db_cursor.execute("DELETE FROM modificationtb WHERE modid=?", (ins_id,))
        

    def tearDown(self):
        self.conn.close()
        
 
if __name__ == '__main__':
    unittest.main()
