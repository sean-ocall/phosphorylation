class Protein(object):
    def __init__(self, uprotid):
        self.uprotid=uprotid
        self.mods = []

    def add_mod(self, mod):
        self.mods.append(mod)

    def add_genename(self, genename):
        self.genename = genename

    def add_function(self, function):
        self.function = function

    def get_uprotid(self ):
        return self.uprotid
    
    def get_genename(self ):
        return self.genename

    def get_function(self ):
        return self.function

    def get_mods(self ):
        return self.mods

    def get_mod(self, index):
        """
        mainly for unittesting
        """
        return self.mods[index]
        

class Modification(object):
    def __init__(self, residue, position, protein):
        self.residue = residue
        self.position = position
        self.protein = protein

    def get_residue(self ):
        return self.residue
    
    def get_position(self ):
        return self.position
    
    def get_protein(self ):
        return self.protein
