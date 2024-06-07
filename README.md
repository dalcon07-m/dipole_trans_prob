##############################################################################################
############################# README  ########################################################
##############################################################################################


#QE orders the output file of dipole moments by k-point, and px, py, pz, transition between the valence and conductions bands

#  P= <phi_c_i | r | phi_v_f>= ihbar/(m*(E_c_i-E_v_f)) <phi_c_i | px, py, pz | phi_v_f>

# Then the output file is ordering as follow: 
#k point (kx,ky,kz),
#component 1=px; 2=py; 3=pz,    
# P^2 top valence---- top conduction, top-1 cond, top-2 cond, bottom conduction.
# P^2 top-1 valence---top conduction, top-1 cond, top-2 cond, bottom conduction.
#  ..       ..           ..               ..         ..           .. 
# P^2 bottom valence---top conduction, top-1 cond, top-2 cond, bottom conduction.

#It is important to know the number of k-points, number of occupied and unoccupied bands.


#################################################################################################
##################################  input parameters ############################################
#################################################################################################



pavg = pd.read_csv('dip_csagincl.dat')  #read the file of P matrix elements
nk = 41  # k-points numbers

nbnd = 50 #number of bands
nbnd_occ = 8  #number of occupied bands
