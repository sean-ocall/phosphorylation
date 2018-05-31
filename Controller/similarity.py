import numpy as np
from read_blosum62 import find_sim_score

def get_score_markers(peptide1, peptide2):
    score_markers = ''

    if len(peptide1) != len(peptide2):
        print "Peptides different lengths: Error"

    else:
        for i, cha in enumerate(peptide1):
            alignment_score = find_sim_score(cha, peptide2[i])
            if alignment_score >= 3:
                score_markers = score_markers + '|'
            elif alignment_score > 0 and alignment_score < 3:
                score_markers = score_markers + ':'
            elif alignment_score < -3:
                score_markers = score_markers + 'x'
            else:
                score_markers = score_markers + ' '

    return score_markers

def get_scores(peptide1, peptide2):
    scores = ''

    if len(peptide1) != len(peptide2):
        print "Peptides different lengths: Error"

    else:
        for i, cha in enumerate(peptide1):
            alignment_score = find_sim_score(cha, peptide2[i])
            if alignment_score >=0:
                str_score = '+' + str(alignment_score)
            else:
                str_score = str(alignment_score)
            scores = scores + str_score

    return scores


def get_similarity_scores(peptides):
    sim_dict = {}
    for peptide in peptides:
        for inner_peptide in peptides:
            if peptide != inner_peptide:
                similarity = smith_waterman(peptide, inner_peptide)
                score_markers = get_score_markers(peptide, inner_peptide)
                sim_dict[peptide + '&&' + inner_peptide +'&&'+ score_markers] = similarity
    return sim_dict

def get_similarity_scores_simple(peptides):
    sim_dict = {}
    for peptide in peptides:
        for inner_peptide in peptides:
            if peptide != inner_peptide:
                similarity = calc_sim_score_simple(peptide, inner_peptide)
                score_markers = get_score_markers(peptide, inner_peptide)
                sim_dict[peptide + '&&' + inner_peptide +'&&'+ score_markers] = similarity
    return sim_dict

def calc_sim_score_simple(peptide1, peptide2):

    sum_score = 0
    
    for aa1, aa2 in zip(peptide1, peptide2):
        score = find_sim_score(aa1, aa2)
        #print score, sum_score
        sum_score = sum_score + score
        
    return sum_score

