#!/usr/bin/python
import os, sys
import re

total_energy = 0.0
log_file = 'grep "E(CORR-CENTRAL)" *out > log_file.txt'
os.system(log_file)
log_file_unit = open('log_file.txt')
result_file = open('final.energy','w')

for eachline in log_file_unit:
    name = eachline.split()[0]
    splitline = re.compile(r'(\w*)\_Sys-(\d*).out\S*')
    sysnum = splitline.search(name)
    energy = float(eachline.split()[2])
    result_file.write('SUBSYSTEM ' + str(sysnum.group(2)) + ': ' + 'E(CENTRAL)=' + str(energy) + '\n')
    total_energy = total_energy + energy


result_file.write('Total Correlation Energy: ' + str(total_energy) + '\n')


test


             
