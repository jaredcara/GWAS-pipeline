#wrapper code

import os                           #imports os module to allow the code to use the command line
import argparse                     #imports the argparse module which accepts input from the command line to use in the running of the code
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser()  #creates the parser list for argparse
#parser.add_argument("test", help="simply a test") #testing argument
args = parser.parse_args()          #creates the list of aruments called args

###STEP 1 - Sex Check#####

#make directory step1 for outputs
os.system("mkdir out")
os.system("mkdir out/step1")
#runs a check sex on data, sends output to step1/step1
os.system("plink --bfile testdata --check-sex -out out/step1/step1")
#finds 'PROBLEM' in output
#this is where the check sex found an issue
os.system("grep 'PROBLEM' out/step1/step1.sexcheck > out/step1/issues.txt")

#open issues
f = open('out/step1/issues.txt', 'r')
s = f.readlines()
f.close()

#in each line, only return the family id and sample id
exclude = []
for each in s:
	this = each.split()
	exclude.append(this[0]+'\t'+this[1])
	
	
#write to testdata/exclude.txt, to be used for down pipe commands	
o = open('out/step1/exclude.txt', 'w')
for each in exclude:
	o.write(each)
	o.write('\n')

o.close()

###STEP 2 - SNP Call Rate###

#SNP call rate
#thresholds set to 0.01

#Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#excludes data from the sex_check
#writes data to step2/step2_1/step2_1

os.system("mkdir out/step2")
os.system("mkdir out/step2/step2_1")
os.system("plink --bfile testdata --exclude out/step1/exclude.txt --missing --out out/step2/step2_1/step2_1")

#recalculates call rate after removing SNPs with call rates <99% and creates a new set of files
#excudes data from the sex_check
#writes data to step2/step2_0/step2_0

os.system("mkdir out/step2/step2_0")
os.system("plink --bfile testdata --exclude out/step1/exclude.txt --geno 0.01 --make-bed --out out/step2/step2_0/step2_0")

##Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#writes data to step2/step2_2/step2_2

os.system("mkdir out/step2/step2_2")
os.system("plink --bfile out/step2/step2_0/step2_0 --missing --out out/step2/step2_2/step2_2")

### STEP 2 -PLOTTING###
x = "out/step2/step2_2" #insert file name here
ftype = ".imiss" #insert file type here

data = pd.read_table(x + ftype, sep= r'\s*') #use panda to read in the data from specified file

plt.figure() #create a new figure
plt.hist(data["F_MISS"], bins = 100) #add a histogram to the figure
plt.xlabel("F_MISS") #add the x label
plt.ylabel("Frequency") #add the y label
plt.title("F_MISS Frequncy Histogram") #add the title
plt.savefig(x + '_histogram.png') #save the file to specified file name as a .png

### STEP 3 - Person Call Rate ###

#make directory for person call rate check output
os.system("mkdir out/step3")
#person call rate with standard 0.1 threshold
#write output to step5/step5
os.system("plink --bfile out/step2/step2_0/step2_0 --mind 0.1 --make-bed --out out/step3/step3")

### STEP 4 - Hardy Weinberg ###

#make directory for hardy-weinberg output
os.system("mkdir out/step4")

#write hardy-weinberg test to step4
#where SNPs with p < 1e-6 are excluded
os.system("plink --bfile out/step2/step2_0/step2_0 --hwe 1e-6 --make-bed -out out/step4/step4")

### STEP 5 - LD prune for relationship check & heterozygosity calculation ###

### STEP 6 - Relationship check ###

### STEP 7 - Heterozygosity check ###
