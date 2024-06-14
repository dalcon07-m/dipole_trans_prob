#!/usr/bin/env python
# coding: utf-8


###  Program to calculate Transition Dipole Moments from the bands.x output of Quantum Espresso##########

import math
import re
import pandas as pd
import numpy as np
import csv

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

soc="yes"   #yes or not, for soc calculation
file_dip="p_avg_soc.dat"

pavg = pd.read_csv(file_dip)  #read the file of P matrix elements
nk = 41  # k-points numbers

nbnd = 100 #number of bands
nbnd_occ = 16  #number of occupied bands

output_file="dip_v_c_soc.dat"
##########################################################################################################################
##### start the program to calculate only the transition dipole moment between bottom conduction and top valence bands####
##########################################################################################################################


kp_pxpypz=[]    #array of k_point and dipolar moments, here I have the k point in (,,,[px,py,pz]) 
nbnd_unocc=nbnd-nbnd_occ   ### number of bands unoccupied


#initialize px, py, pz variable to after append to kp_pxpypz 

px=0  
py=0
pz=0

pxs=0 #for soc
pys=0 
pzs=0 

il = math.ceil(nbnd_unocc/5) #integer division, number of lines per px, py, pz ----9, here we start with the first element px
rowbycol=il*nbnd_occ   #number of row per component x,y,z  

#if file_dip == "p_avg_soc.dat" #to take into account the soc, spin up-down for ech band

 #   il = math.ceil((2*nbnd_unocc)/5) #in the case of soc, to select the other valence band
  #  rowbycol=int(il*nbnd_occ/2)  #for soc

ild=0  #first kpoint
dm=il  ##dumb variable to define ild



###########


for dumb in range(0,nk):   #to all the k-points   
    
    k_line = pavg.iloc[ild,0].split()    #il is the line number, here I divide the data
    kp_pxpypz.append([k_line[0],k_line[1],k_line[2]]) #this is to save the k point from k_line
   
    il +=1    ##output P file start wit the matrices values in the second line!
    
    for ipol in range(3):  ###range 3 for ipol=0,1,2, for px,py,pz
        tmp = pavg.iloc[il,0].split() 
       
        if ipol == 0:
            px=tmp[-1]  #select the last element corresponding to the bottom valence
            if len(tmp)==1:  #in the case of just one element in the last row
                print('length is 1')
                tmps=pavg.iloc[il-1,0].split()
                pxs=tmps[-1]
            else:
                pxs=tmp[-2] #for soc  v spinup-- c spin up, down  
           #select the last element corresponding to the bottom valence
        elif ipol == 1:
            py=tmp[-1]
            if len(tmp)==1:  #in the case of just one element in the last row
                tmps=pavg.iloc[il-1,0].split()
                pys=tmps[-1]
            else:
                pys=tmp[-2]
        else:
            pz=tmp[-1]
            if len(tmp)==1:  #in the case of just one element in the last row
                tmps=pavg.iloc[il-1,0].split()
                pzs=tmps[-1]
            else:
                pzs=tmp[-2]
        il=il+(rowbycol+1)  ## +1 because of the line with 1,2 or3    
        
         
    ild=il-dm   #to calculate the new k-point
    #print('ild', ild)    

    if soc == "yes":
        px=float(px)+float(pxs)
        py=float(py)+float(pys)
        pz=float(pz)+float(pzs)

    kp_pxpypz[-1].append([px, py, pz])  #here is the matrix with the k-point and the corresponding dipole matrices
    

###########################################################################################################################
############# Now, to define the k_point like the bands.f90 from QE  ######################################################
###########################################################################################################################
kp=[0]  #first array  element 

dxmod_save=1 #to initialize the variable

for n in range(1,nk):

    dxmod=math.sqrt(pow(float(kp_pxpypz[n][0])-float(kp_pxpypz[n-1][0]),2)+pow(float(kp_pxpypz[n][1])-float(kp_pxpypz[n-1][1]),2)+pow(float(kp_pxpypz[n][2])-float(kp_pxpypz[n-1][2]),2))
    if dxmod > 5*dxmod_save:
        kp.append(kp[n-1])
    elif dxmod > 1e-4:
        kp.append(kp[n-1]+dxmod)
        dxmod_save=dxmod
    else:
        kp.append(kp[n-1]+dxmod)

# the k-points like bands.dat.gnu are in kp array

##########################################################
## now to organize the data for plot in gnuplot ##########
##########################################################



with open(output_file, 'w') as archivo:
    for kpoint, px in zip(kp,kp_pxpypz):    #here we go for all the elements in kp_pxpypx and print the information to plot
        print(kpoint, end=" ", file=archivo )
        print(px[3][0],px[3][1] ,px[3][2], file=archivo) # finally print the data to plot

print('The output file is printed in', output_file)




# In[ ]:




