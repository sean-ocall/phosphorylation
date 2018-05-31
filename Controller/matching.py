try:
    from mpi4py import MPI
except:
    print "No mpi4py installed: serial execution only"



def find_associated_by_sequence(phosphosites, cutoff=20):
    """
    
    """
    try:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        iters_per_rank = int(float(len(phosphosites))/size)
        print "Iters per rank:", iters_per_rank
        if rank == 0:
            limits = [0, iters_per_rank]
        elif rank > 0 and rank < size-1: # If not the last rank
            limits = [(rank*iters_per_rank)+1, (rank+1)*iters_per_rank]
            print rank, ":", limits
        else: # last rank, finish at end
            limits = [rank*iters_per_rank, len(phosphosites)]
            print rank, ":", limits
        
    except:
        rank = 0
        limits = [0,len(phosphosites)]
     

    
    print "Number of phosphositetb entries:", len(phosphosites)
    counter = 0
    
    matches = []

    copy_psites = copy.deepcopy(phosphosites) # Is this necessary???

    print "Processing from",limits[0],"to",limits[1]
    t1 = time.time()
    for psite in phosphosites[limits[0]:limits[1]]:
        similar_sites = []
        for copy_psite in copy_psites:
            possible_match_sequence = copy_psite.get_AA_sequence()
            anchor_sequence = psite.get_AA_sequence()
            if '-' not in possible_match_sequence and '-' not in anchor_sequence:
                if calc_sim_score_simple(possible_match_sequence, anchor_sequence)\
                   > cutoff:
                    similar_sites.append(copy_psite)
        match = Match(psite, similar_sites)
        matches.append(match)
        
        counter = counter + 1
    t2 = time.time()
    print "Did", counter, "iterations on rank", rank, "equals", (t2-t1)/counter,"secs per iteration"

    if rank == 0:
        for r in range(1,size):
            more_matches = comm.recv(source=r)
            for m in more_matches:
                matches.append(m)
    else:
        print "sending", limits[0], "to", limits[1]
        comm.send(matches, dest=0)

    if rank == 0:
        return matches



if __name__=="__main__":
    conn = sqlite3.connect(sys.argv[1])
    db_cursor = conn.cursor()

    db_cursor.execute("SELECT * FROM phosphositetb")
    psite_tb_results = db_cursor.fetchall()
    phosphosites = []
    # t_fields = ['residue', 'position', 'uniprotid','genename','function', 'foldchange', 'AA_sequence']
    #                0           1            2          3          4            5             6
    # def __init__(self, residue, position, uniprotid, fold_change):
    for psite in psite_tb_results:
        new_psite = Phosphosite(psite[0],psite[1],psite[2],psite[5])
        new_psite.set_AA_sequence(psite[6])
        phosphosites.append(new_psite)

    phosphosites_reduced = phosphosites[0:300] # For testing purposes    
    #matches = find_associated_by_sequence(mods_reduced)

    t1 = time.time()
    matches = find_associated_by_sequence(phosphosites_reduced)
    t2 = time.time()
    print "Time taken: ", t2-t1
    
    
    
    #try:
    #    comm = MPI.COMM_WORLD
    #    rank = comm.Get_rank()
    #    if rank == 0:
    #        find_all_genenames_from_matches(matches)
    #        for match in matches:
    #            match.add_matches_to_db(db_cursor)
    #            print match

    # We want to present:
    #
    #   ----anchor mod-----↑
    #
    #   ----related 1------↑
    #   ----related 2------↓
    #   ----related 3------↓
    #         etc
    #         etc
    #
    # so will need fold change and relationships info

    # Next to do: set up Match class and associated functions/methods
