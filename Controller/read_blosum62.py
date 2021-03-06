"""
BLOSUM62 is a widely used similarity matrix for comparing amino acid sequences

Certain substitutions are far more likely than others to occur, e.g. Glutamic Acid and Aspartic Acid.

This code captures the BLOSUM62 matrix and makes it available in a Python
dictionary of dictionaries

author: Sean O'Callaghan
date: 22 Feb '18
"""


def read_blosum(blosum_file):

    fp = open(blosum_file,'r')

    position_x_dict = {}

    lines = fp.readlines()

    for i,part in enumerate(lines[0].lstrip().split()):
        position_x_dict[i] = part

    #for key, value in position_x_dict.iteritems():
    #    print key, ':', value

    blosum_matrix = {}

    for line in lines[1:]:
        inner_dict = {}
        parts = line.split()
        for i, part in enumerate(parts[1:]):
            inner_dict[position_x_dict[i]] = part
        blosum_matrix[parts[0]] = inner_dict

    #for key, value in blosum_matrix.iteritems():
    #    # for testing just check L
    #    if key == 'L':
    #        print key,
    #    for in_key, in_value in value.iteritems():
    #        print in_key, ":", in_value,
    #    print ''

    return blosum_matrix


def find_sim_score(aa_1, aa_2, blosum_file="BLOSUM62.txt", silence=True):
    aa_1 = aa_1.upper()
    aa_2 = aa_2.upper()
    blosum_matrix = read_blosum(blosum_file)
    aa_list = ['A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']

    if aa_1 not in aa_list or aa_2 not in aa_list:
        if not silence:
            print "One of your amino acid codes is not valid:", aa_1, aa_2
        return 'NA'
    else:
        score_list = blosum_matrix[aa_1]
        score = score_list[aa_2]
        return int(score)


if __name__ == "__main__":
    blosum_matrix = read_blosum("BLOSUM62.txt")
    score = find_sim_score('L', 'I', blosum_matrix)
    if score == 2:
        print "score for 'L':'I' is 2, correct"
    else:
        print "incorrect score", score, "for 'L':'I', should be 2"
    
