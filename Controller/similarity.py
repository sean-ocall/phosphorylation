import numpy as np
from alignment.alignment import needle

def smith_waterman(a, b, alignment_score = 1.0, gap_cost = 1.0):
    """
    Compute the Smith-Waterman alignment score for two strings.
    See https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm#Algorithm
    This implementation has a fixed gap cost (i.e. extending a gap is considered
    free). In the terminology of the Wikipedia description, W_k = {c, c, c, ...}.
    This implementation also has a fixed alignment score, awarded if the relevant
    characters are equal.
    Kinda slow, especially for large (50+ char) inputs.
    """
    # H holds the alignment score at each point, computed incrementally
    H = np.zeros((len(a) + 1, len(b) + 1))
    for i in range(1, len(a) + 1):
      for j in range(1, len(b) + 1):
        # The score for substituting the letter a[i-1] for b[j-1]. Generally low
        # for mismatch, high for match.
        match = H[i-1,j-1] + (alignment_score if a[i-1] == b[j-1] else 0)
        # The scores for for introducing extra letters in one of the strings (or
        # by symmetry, deleting them from the other).
        delete = H[1:i,j].max() - gap_cost if i > 1 else 0
        insert = H[i,1:j].max() - gap_cost if j > 1 else 0
        H[i,j] = max(match, delete, insert, 0)
    # The highest score is the best local alignment.
    # For our purposes, we don't actually care _what_ the alignment was, just how
    # aligned the two strings were.
    return H.max()


def get_peptides():
    # place holder until we start grabbing from database
    peptide_string = """
[R].MSESPTPCSGSSFEETEALVNTAAK.[N]
[K].TSFDQDSDVDIFPSDFPTEPPSLPR.[T]
[K].CDSSPDSAEDVRK.[V]
[-].MNLLPNIESPVTRQEK.[M]
[R].EAANEAGDSSQDEAEDDVK.[Q]
[R].TPGVLLPGAGGAAGFGMTSPPPPTSPSR.[T]
[-].MEPSSWSGSESPAENMER.[M]
[K].TPEANSRASSPCPEFEQFQIVPAVETPYLAR.[A]
[R].TKLHQLSGSDQLESTAHSR.[I]
[-].MENALTGSQSSHASLRNIHSINPTQLMAR.[I]
[K].LTSSCPDLPSQTDKK.[C]
[K].TGVTSTSDSEEEGDDQEGEK.[K]
[R].SDSHSRSLSPNHNTLQTLK.[S]
[K].NAPPGGDEPLAETESESEAELAGFSPVVDVKK.[T]
[R].GHTASESDEQQWPEEKR.[L]
[K].ITFITSFGGSDEEAAAAAAAAAASGVTTGKPPAPPQPGGPAPGR.[N]
[R].LSVGSVTSRPSTPTLGTPTPQTMSVSTK.[V]
[K].SSSLESLQTAVAEVTLNGDIPFHRPRPR.[I]
[R].SDSPEIPFQAAAGPSDGLDASSPGNSFVGLR.[V]
[K].HLDGEEDGSSDQSQASGTTGGR.[R]
[R].HLLTDLPLPPELPGGDLSPPDSPEPK.[A]
[R].SMVSPVPSPTGTISVPNSCPASPR.[G]
[R].SLSRTPSPPPFR.[G]
[R].LASDSDAESDSRASSPNSTVSNTSTEGFGGIMSFASSLYR.[N]
[R].LGSPDYGNSALLSLPGYRPTTR.[S]
[K].ICTEQSNSPPPIR.[R]
[R].IDPWSFVSAGPRPSPLPSPQPAPR.[R]
[R].STSPSDSLPCSLAGSPAPSPAPSPAPAGL.[-]
[K].SASSESEAENLEAQPQSTVRPEEIPPIPENR.[F]
[R].SLSELCLAVPAPGIR.[T]
[R].AQSGSDSSPEPKAPAPR.[A]
[R].ALIRSPSLAK.[Q]
[R].NSSSAGSGSGDPSEGLPR.[R]
[R].QLARSCLDLNTISQSPGWAQTQLAEVTIACK.[V]
[R].ALSPLPTR.[T]
[K].AASEQQADTSGGDSPKDESKPPFSYAQLIVQAISSAQDR.[Q]
[R].YLESVRPLLDDEEYYRMELLAK.[E]
[R].VALSDDETKETENMR.[K]
    """
    raw_peptides = peptide_string.split('\n')
    peptides = [peptide[4:-4] for peptide in raw_peptides]
    del peptides[0] #get rid of blanks caused by extra \n's
    del peptides[-1]
    return peptides

def get_similarity_scores(peptides):
    sim_dict = {}
    for peptide in peptides:
        for inner_peptide in peptides:
            if peptide != inner_peptide:
                similarity = smith_waterman(peptide, inner_peptide)
                sim_dict[peptide + '&&' + inner_peptide] = similarity
    return sim_dict

def get_similarity_scores_needle(peptides):
    sim_dict = {}
    for peptide in peptides:
        for inner_peptide in peptides:
            if peptide != inner_peptide:
                similarity = needle(peptide, inner_peptide)
                sim_dict[peptide + '&&' + inner_peptide] = similarity
    return sim_dict


def write_output(sim_dict):
    op = open('similarity_matrix.csv','w')
    op.write("Peptide1, Peptide2, sim score\n")

    for key,value in sim_dict.iteritems():
        peptides = key.split('&&')
        print peptides, value
        op.write(peptides[0] + ','+ peptides[1] + ',' + str(value) + '\n')
    op.close()

if __name__ == "__main__":
    #a = "ATAGACGACATACAGACAGCATACAGACAGCATACAGA"
    #b = "TTTAGCATGCGCATATCAGCAATACAGACAGATACG"

    #H = smith_waterman(a,b)
    #print "Similarity is ",H
    peptides = get_peptides()
    sim_dict = get_similarity_scores_needle(peptides)
    write_output(sim_dict)
    
