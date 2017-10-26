import argparse, sqlite3, os
from jinja2 import Environment, FileSystemLoader

help_msg = "Grabs data from DB and renders to html"
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument('--databasefile', help='sqlite3 file (or blank)')

def render_table(proteins_dict):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print j2_env.get_template('templates/table.jj2').render\
        (proteins=proteins_dict)

def get_proteins_from_db(db_cursor):
    proteins_cursor = db_cursor.execute("SELECT * FROM proteintb;")
    proteins = proteins_cursor.fetchall()

    proteins_listofdicts = []
    
    for protein in proteins:
        p_dict = {}
        p_dict['proteinid'] = protein[0]
        p_dict['uniprotid'] = protein[1]
        p_dict['genenameid'] = protein[2]
        p_dict['function'] = protein[3]

        proteins_listofdicts.append(p_dict)

    return proteins_listofdicts

def render():
    # Takes the place of __main__ for now in mod_python
    conn = sqlite3.connect("/home/phospho/phosphorylation/Model/phospho-db.sqlite")
    db_cursor = conn.cursor()

    proteins_listofdicts = get_proteins_from_db(db_cursor)
    render_table(proteins_listofdicts)

    conn.close()

if __name__=="__main__":
    args = parser.parse_args()
    conn = sqlite3.connect(args.databasefile)
    db_cursor = conn.cursor()

    proteins_listofdicts = get_proteins_from_db(db_cursor)
    render_table(proteins_listofdicts)

    conn.close()
    
