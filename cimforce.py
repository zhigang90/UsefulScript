#!/usr/bin/python
import os, sys
import re

total_energy = 0.0
outfiles = 'grep "Atom  Name FullLabel" *Sys*out > outfiles.txt'
os.system(outfiles)
out_file_unit = open('outfiles.txt')
result_file = open('finalforce.txt','w')

# Get the number of atoms of the whole molecule
for eachline in out_file_unit:
    name = eachline.split(':')[0]
    splitline = re.compile(r'(\w*)\_Sys-(\d*).out\S*')
    sysnum = splitline.search(name)
    moname = sysnum.group(1)
    moout = moname + '.out'
    output = open(moout)
    for line in output:
        if line[3:21] == 'Number of symmetry':
            ntotatom = int(line.splat(':')[1])
            break
    break
out_file_unit.seek(0)

force = {}
for atom in range(1,ntotatom+1):
    force[atom]=[0,0,0]

for eachline in out_file_unit:
    name = eachline.split(':')[0]
    splitline = re.compile(r'(\w*)\_Sys-(\d*).out\S*')
    sysnum = splitline.search(name)
    outfile = open(name)
    find_start = 0
    force_get = 0
    for line in outfile:
        if line[3:21] == 'Number of symmetry':
            natom = int(line.split(':')[1])
        if line[1:11] == 'Atom  Name':
            find_start = 1
            continue
        
        if find_start == 1: 
           if line == '\n':
               continue
           else:
               force_get = force_get + 1
               atomlabel = int(line.split()[2])
               for i in range(0,3):
                   force[atomlabel][i] += float(line.split()[i+3])
               if force_get == natom:
                   break

for i in range(1,ntotatom+1):
    result_file.write(str('%4d'%i)+str('%11.7f'%(force[i][0])) +str('%11.7f'%(force[i][1]))+str('%11.7f'%(force[i][2])) +'\n')
