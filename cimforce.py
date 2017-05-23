#!/usr/bin/python
import os, sys
import re

class atomforce:
    def __intit__(self):
        self

total_energy = 0.0
outfiles = 'grep "Atom  Name FullLabel" *Sys*out > outfiles.txt'
os.system(outfiles)
out_file_unit = open('outfiles.txt')
result_file = open('finalforce.txt','w')


for eachline in out_file_unit:
    name = eachline.split(':')[0]
    splitline = re.compile(r'(\w*)\_Sys-(\d*).out\S*')
    sysnum = splitline.search(name)
    moname = sysnum.group(1)
    moout = moname + '.out'
    output = open(moout)
    for line in output:
        if line[3:21] == 'Number of symmetry':
            ntotatom = line.split(':')[1]
            break
    break
force = {}
for atom in range(0,ntotatom):
    force[atom]=[0,0,0]

for eachline in out_file_unit:
    name = eachline.split(':')[0]
    splitline = re.compile(r'(\w*)\_Sys-(\d*).out\S*')
    sysnum = splitline.search(name)
    outfile = open(name)
    find_start = 0
    force_get = 0
    force = [] []
    for line in outfile:
        if line[3:21] == 'Number of symmetry':
            natom = line.split(':')[1]

        if line[1:12] == 'Atom  Name':
            find_start = 1
            continue
        
        if find_start == 1: 
           if line == '':
               continue
           else:
               force_get = force_get + 1
               line.split()



    energy = float(eachline.split()[2])
    result_file.write('SUBSYSTEM ' + str(sysnum.group(2)) + ': ' + 'E(CENTRAL)=' + str(energy) + '\n')
    total_energy = total_energy + energy
result_file.write('Total Correlation Energy: ' + str(total_energy) + '\n')

test
             
