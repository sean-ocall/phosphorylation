import sqlite3
conn = sqlite3.connect('../Model/phospho-db.sqlite')
c = conn.cursor()

table_name = 'phosphositetb'
#              0           1           2           3         4            5              6
t_fields = ['residue', 'position', 'uniprotid','genename','function', 'foldchange', 'AA_sequence']
t_field_types = ['TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'FLOAT','TEXT']

c.execute(""" CREATE TABLE IF NOT EXISTS {tn} (
                                        {fn1} {ft1},
                                        {fn2} {ft2},
                                        {fn3} {ft3},
                                        {fn4} {ft4},
                                        {fn5} {ft5},
                                        {fn6} {ft6},
                                        {fn7} {ft7}
                                    ); """.format(tn=table_name,
                                                  fn1=t_fields[0],
                                                  fn2=t_fields[1],
                                                  fn3=t_fields[2],
                                                  fn4=t_fields[3],
                                                  fn5=t_fields[4],
                                                  fn6=t_fields[5],
                                                  fn7=t_fields[6],
                                                  ft1=t_field_types[0],
                                                  ft2=t_field_types[1],
                                                  ft3=t_field_types[2],
                                                  ft4=t_field_types[3],
                                                  ft5=t_field_types[4],
                                                  ft6=t_field_types[5],
                                                  ft7=t_field_types[6]))
conn.commit()
conn.close()
