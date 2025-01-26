'''
This is a script written in python 3, which main goal is provide the user
with the log (output) files created during the decomposition of a target
molecule with AutoMeKin, but with the names that are actually used in the MINinfo, TSinfo
and now PRODinfo files.

This script was written by Marta Castiñeira , l.u. 04/12/2023
'''

#------------------------------------------------------------------------------#
#                     Section to import modules                                #
#------------------------------------------------------------------------------#
import os
import sqlite3
import shutil

#------------------------------------------------------------------------------#
#                     Section to confirm user is in the right folder (Main)               #
#------------------------------------------------------------------------------#

# Confirming existence of FINAL and tsdir
if not any(item.startswith("FINAL_HL") for item in os.listdir()):
    raise FileNotFoundError("FINAL directory is missing. Are you in the main dir?")
else:
    print("FINAL directory found.")

if not any(item.startswith("tsdirHL") for item in os.listdir()):
    raise FileNotFoundError("tsdir directory is missing. Are you in the main dir?")
else:
    print("tsdir directory found.")


#------------------------------------------------------------------------------#
#                     Section to define some important variables               #
#------------------------------------------------------------------------------#

for i in os.listdir():
    if i.startswith("FINAL_HL")== True:
        folder_HL = i+"/"

for archo in os.listdir():
    if archo.startswith("tsdirHL")== True:
        tsdirHL = archo+"/"

# we create a folder to incorporate our renamed files:
if not os.path.exists("OUTPUT/"):
    os.mkdir("OUTPUT/")
    print("OUTPUT directory created")  
else:  
    print("OUTPUT directory was already created")

#------------------------------------------------------------------------------#
#                      Sections for functions                                  #
#------------------------------------------------------------------------------#

def mints_rename(folder_HL):
    #we stablish the equivalence between names
    os.chdir(folder_HL) 

    # we start copying the mins
    cur=sqlite3.connect("min.db") #initiating a connection with the database

    # we extract the equivalence between names from the db
    for row in cur.execute("select id,natom,name,lname,energy,zpe,g,geom,freq from min"):
               old_name = "_".join(row[3].split(".")[0].split("_")[1:])+".log"
               #new_name = 'MIN{:0>3d}'.format(row[0]) 
               new_name = "MIN"+str(row[0]) 
               print(new_name,old_name)
               shutil.copyfile("../"+tsdirHL+"IRC/"+old_name,"../OUTPUT/"+new_name+".out") 

    # we extract the equivalence between names from the db
    # we continue with copying the tss
    cur=sqlite3.connect("ts.db") #initiating a connection with the database
    for row in cur.execute("select id,natom,name,lname,energy,zpe,g,geom,freq from ts"):
               old_name = "_".join(row[3].split(".")[0].split("_")[1:])+".log"
               #new_name = 'TS{:0>3d}'.format(row[0]) 
               new_name = "TS"+str(row[0]) 
               print(str(row[2]).zfill(3),old_name)
               shutil.copyfile("../"+tsdirHL+old_name,"../OUTPUT/"+new_name+".out") 
    os.chdir("../") 
                

def prods_rename(folder_HL):
    #we stablish the equivalence between names
    os.chdir(folder_HL) 

    # we start copying the mins
    cur=sqlite3.connect("prod.db") #initiating a connection with the database

    # we extract the equivalence between names from the db
    for row in cur.execute("select id,natom,name,energy,zpe,g,geom,freq,formula from prod"):
               old_name = "_".join(row[2].split("_")[1:])+".log"
               new_name = '{:0>3}'.format(row[2].split("_")[0]+"_SP")
               print(new_name.zfill(3),old_name)

               #here we must make a separation between those prods comming from a barrierless (AMK definition) path
               #and those coming from a path with a barrier.
               if "diss" not in old_name:
                         shutil.copyfile("../"+tsdirHL+"IRC/"+old_name,"../OUTPUT/"+new_name+".out") 

               if "diss" in old_name:
                         shutil.copyfile("../"+tsdirHL+"IRC/DISS/"+old_name,"../OUTPUT/"+new_name+".out") 

    os.chdir("../") 

def prods_rename_opt():
    #we stablish the equivalence between names
    os.chdir(tsdirHL+"PRODs/") 
    with open('PRlist_frag','r') as asdf:
         for line in asdf:
             line = line.split()
             if line[1] != "list":
                 new_name_a = "PR"+str(line[1])+"_a"
                 new_name_b = "PR"+str(line[1])+"_b"
                 name_frag_a = str(line[3])+".log"
                 name_frag_b = str(line[5])+".log"

                 try: 
                       shutil.copyfile("CALC/"+name_frag_a,"../../OUTPUT/"+new_name_a+".out") 
                       print("OK,",name_frag_a," copied to: ",new_name_a)
                 except:
                       print("This fragment is not computed",name_frag_a)

                       with open('CALC/working/fraglist','r') as asdf:
                            for line in asdf:
                                 line = line.strip().split()
                                 if line[1] == name_frag_a[:-4]:
                                      shutil.copyfile("CALC/"+line[2]+".log","../../OUTPUT/"+new_name_a+".out")
                                      print("OK, trouble solved..,",line[2]+".log"," copied to: ",new_name_a)
                                      break
                       asdf.close()               

                 try: 
                       shutil.copyfile("CALC/"+name_frag_b,"../../OUTPUT/"+new_name_b+".out") 
                       print("OK,",name_frag_b," copied to: ",new_name_b)
                 except:
                       print("This fragment is not computed",name_frag_b)
                       with open('CALC/working/fraglist','r') as asdf:
                            for line in asdf:
                                 line = line.strip().split()
                                 if line[1] == name_frag_b[:-4]:
                                      shutil.copyfile("CALC/"+line[2]+".log","../../OUTPUT/"+new_name_b+".out")
                                      print("OK, trouble solved..,",line[2]," copied to: ",new_name_b)
                                      break
                       asdf.close()               
             continue

    

    
#------------------------------------------------------------------------------#
#                        Here we operate the functions                         #
#------------------------------------------------------------------------------#
mints_rename(folder_HL)
prods_rename(folder_HL)
prods_rename_opt()
