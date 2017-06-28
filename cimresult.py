#!/usr/bin/python
import os, sys
import shutil
import re

try:
    name = sys.argv[1]
except ValueError:
    print 'Please input the name of the input file (without surfix).'
    sys.exit(2)

submtd = 'MP2'
dislmo = 5.5
virthr = 0.05
calforce = False
inputfile = open(name + '.inp')
for line in inputfile:
    if line[0:3].lower() == 'cim':
        keywords = line.split()
        break
for keyword in keywords:
    key = keyword.lower()[0:4]
    if key == 'subm':
        submtd = keyword.split('=')[1]
    elif key == 'disl':
        dislmo = float(keyword.split('=')[1])
    elif key == 'virt':
        virthr = float(keyword.split('=')[1])
    elif key == 'forc':
        calforce = True

tot_output = open(name + '.out')
cim_output = open(name + '.cim','w')
force_found = False
force_not_done = True
force_get = 0
scf_force = {}
for line in tot_output:
    if line[3:21] == 'Number of symmetry':
        ntotatom = int(line.split(':')[1])
        continue

    if line[1:13] == 'Total Energy':
        scf_energy = float(line.split()[3])
        continue

    if line[1:10] == 'Atom Name':
        force_found = True
        continue

    if force_found and force_not_done:
        if line == '\n': 
            continue
        else:
            force_get += 1
            forceline = line.split()
            scf_force[int(forceline[0])] = forceline[1:]
            if force_get == ntotatom:
                force_not_done = False
                continue
            
    if line[1:25] == 'Final number of clusters':
        ncluster = int(line.split(':')[1])
        break

corr_energy = 0.0
if calforce:
    corr_force = {}
    for atom in range(1,ntotatom+1):
        corr_force[atom]=[0,0,0]

for i in range(1,ncluster+1):
    subforce_found = -1
    suboutname = name + '_Sys-' + str(i) + '.out'
    subout = open(suboutname)
    for line in subout:
        if line[0:16] == ' E(CORR-CENTRAL)':
            sub_energy = float(line.split()[1])
            corr_energy += sub_energy
            continue
        if calforce:
            if line[3:21] == 'Number of symmetry':
                nsubatom = int(line.split(':')[1])
                continue
            if line[1:27] == 'Two-electron contributions':
                subforce_found = 0
                continue
            if subforce_found > -1:
                if line == '\n' or line[1:11] == 'Atom  Name':
                    continue
                else:
                    subforce_found += 1
                    atomlabel = int(line.split()[2])
                    for j in range(0,3):
                        corr_force[atomlabel][j] += float(line.split()[j+3])
                    if subforce_found == nsubatom:
                        break                    
    subout.close()

cim_output.write('CIM Calculation Results!\n\n')
cim_output.write('Parameters:\n')
cim_output.write('===========\n')
cim_output.write('SubMethod : ' + submtd.upper() + '\n')
cim_output.write('DisLMO    :' + str('%5.2f' % dislmo) + '\n')
cim_output.write('VirThresh :' + str('%5.2f' % virthr) + '\n')
cim_output.write('\n')
cim_output.write('Energy Results:\n')
cim_output.write('===============\n')
cim_output.write('E(SCF)  =' + str('%16.9f' % scf_energy) + '\n')
cim_output.write('E(Corr) =' + str('%16.9f' % corr_energy) + '\n')
cim_output.write('E(Total)=' + str('%16.9f' % (scf_energy + corr_energy)) + '\n\n')
if calforce:
    cim_output.write('Force Results:\n')
    cim_output.write('==============\n')
    cim_output.write('SCF Forces:\n')
    cim_output.write('Atom  Name     force-x     force-y     force-z\n')
    for i in range(1,ntotatom+1):
        cim_output.write(str('%4d' % i) + '   ' + scf_force[i][0].capitalize() + '   ' + '%12s'%scf_force[i][1] + '%12s'%scf_force[i][2] + '%12s'%scf_force[i][3] + '\n')
    cim_output.write('\nCorr Forces:\n')
    cim_output.write('Atom  Name     force-x     force-y     force-z\n')
    total_force = {}
    for i in range(1,ntotatom+1):
        total_force [i] = [0,0,0]
        for j in range(0,3):
            total_force [i][j] = float(scf_force[i][j+1]) + corr_force[i][j] 
        cim_output.write(str('%4d' % i) + '   ' + scf_force[i][0].capitalize() + '   ' + str('%12.7f' % corr_force[i][0]) + str('%12.7f' % corr_force[i][1]) + str('%12.7f' % corr_force[i][2]) + '\n')
    cim_output.write('\nTotal Forces:\n')
    cim_output.write('Atom  Name     force-x     force-y     force-z\n')
    for i in range(1,ntotatom+1):
        cim_output.write(str('%4d' % i) + '   ' + scf_force[i][0].capitalize() + '   ' + str('%12.7f' % total_force[i][0]) + str('%12.7f' % total_force[i][1]) + str('%12.7f' % total_force[i][2]) + '\n')
    
