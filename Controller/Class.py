class Phosphosite(object):
    def __init__(self, residue, position, uniprotid, fold_change):

        self.residue = residue
        self.position = position
        self.uniprotid = uniprotid
        self.fold_change = fold_change

    def set_rowid(self, rowid):
        self.rowid = rowid

    def get_rowid(self):
        return self.rowid

    def get_residue(self ):
        return self.residue
    
    def get_position(self ):
        return self.position
    
    def get_uniprotid(self ):
        return self.uniprotid

    def get_fold_change(self):
        return self.fold_change

    def set_AA_sequence(self, AA_sequence):
        self.AA_sequence = AA_sequence
    
    def get_AA_sequence(self ):
        return self.AA_sequence

    def set_genename(self, genename):
        self.genename = genename

    def get_genename(self):
        return self.genename

    def set_function(self, function):
        self.function = function

    def get_function(self):
        return self.function
    
    def get_label(self):
        return u"{}".format(self.genename) + ' ' + self.residue + str(self.position)
