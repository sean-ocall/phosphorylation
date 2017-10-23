import sqlite3
conn = sqlite3.connect('phospho-db.sqlite')
c = conn.cursor()

table_name1 = 'proteintb'  # name of the table to be created
table_name2 = 'modificationtb'  # name of the table to be created
t1_fields = ['proteinid','uniprotid','genename','function']
t1_field_types = ['INTEGER','TEXT','TEXT','TEXT']  # column data type

t2_fields = ['modid','residue', 'position', 'proteinid']
t2_field_types = ['INTEGER','TEXT', 'INTEGER', 'INTEGER']


# Creating proteintb
c.execute(""" CREATE TABLE IF NOT EXISTS {tn} (
                                        {fn1} {ft1} PRIMARY KEY,
                                        {fn2} {ft2},
                                        {fn3} {ft3},
                                        {fn4} {ft4}
                                    ); """.format(tn=table_name1,
                                                  fn1=t1_fields[0],
                                                  fn2=t1_fields[1],
                                                  fn3=t1_fields[2],
                                                  fn4=t1_fields[3],
                                                  ft1=t1_field_types[0],
                                                  ft2=t1_field_types[1],
                                                  ft3=t1_field_types[2],
                                                  ft4=t1_field_types[3]))
c.execute(""" CREATE TABLE IF NOT EXISTS {tn} (
                                        {fn1} {ft1} PRIMARY KEY,
                                        {fn2} {ft2},
                                        {fn3} {ft3},
                                        {fn4} {ft4}
                                    ); """.format(tn=table_name2,
                                                  fn1=t2_fields[0],
                                                  fn2=t2_fields[1],
                                                  fn3=t2_fields[2],
                                                  fn4=t2_fields[3],
                                                  ft1=t2_field_types[0],
                                                  ft2=t2_field_types[1],
                                                  ft3=t2_field_types[2],
                                                  ft4=t2_field_types[3]))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
