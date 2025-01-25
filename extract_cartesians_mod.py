
#This is a script written in python3 that creates cartesian coordinate files
#for each min, ts, prodi_fraga, prodi_fragb. This step should be very
#useful for comparison purposes. PLEASE!, execute this code inside your FINAL_HL folder, or a folder containing
#the databases, min.db, ts.db and prod.db. To execute this script, you should have
#previously loaded the automekin and its dependencies. Also, you should use python 3
#l.u. 12/07/2023

#---------------------------------------------------------------------#
#   section for importing libraries
#---------------------------------------------------------------------#
#Importing modules for a python 3 script

import sqlite3

#---------------------------------------------------------------------#
#        section to keep track of functions
#---------------------------------------------------------------------#

def THEMINTSDATABASE(database):
        cur=sqlite3.connect(database) #creamos conexion con la base de datos que queremos crear
        if  "min" in str(database):
              n=0
              for row in cur.execute("select id,natom,name,lname,energy,zpe,g,geom,freq from min"):
                n +=1
                with open("MIN"+str(n)+".xyz", 'w') as adf:
                         adf.write(str(row[1])+'\n'+'\n')
                         adf.write(str(row[7]))
                         #adf.close()
                name = "MIN"+str(n)
                fnum_atom  =  str(row[1])
                natom = int(row[1])
                geom = row[7]

        elif  "ts" in str(database):
              n=0
              for row in cur.execute("select id,natom,name,lname,energy,zpe,g,geom,freq from ts"):
                n +=1
                with open("TS"+str(n)+".xyz", 'w') as adf:
                         adf.write(str(row[1])+'\n'+'\n')
                         adf.write(str(row[7]))
                name = "TS"+str(n)
                fnum_atom  =  str(row[1])

#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
def THEPRDATABASE():
        #1. Lets open the database and start reading it (PRODUCTS)
        cur=sqlite3.connect("prod.db") #creamos conexion con la base de datos que queremos crear
        values = []
        row_num = -1
        conmat_str = ""
        for row in cur.execute("select id,natom,name,energy,zpe,g,geom,freq,formula from prod"):
                geom = row[6]
                number_atoms = row[1]
                row_num2 = int(row[0])
                row_num += 1
                name = row[2]
                line = ""
                line2 = ""
                line3 = ""
                values = []
                conmat_str = ""

                file1 = open("PR"+str(row[0])+".xyz", 'w')
                file1.write(str(row[1]))
                file1.write('\n')
                file1.write('\n')
                file1.write(row[6])
                file1.write('\n')
                file1.close()


#---------------------------------------------------------------------#
#        section to operate the functions
#---------------------------------------------------------------------#
THEMINTSDATABASE('min.db')
THEMINTSDATABASE('ts.db')
THEPRDATABASE()








