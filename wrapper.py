#wrapper code

import os                           #imports os module to allow the code to use the command line
import argparse                     #imports the argparse module which accepts input from the command line to use in the running of the code
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser()  #creates the parser list for argparse
parser.add_argument('fil', help="enter file name ex. '/home/user/desktop/infile' without extentions")
#parser.add_argument("test", help="simply a test") #testing argument
args = parser.parse_args()          #creates the list of aruments called args

fil = args.fil

###STEP 1 - Sex Check#####

#make directory step1 for outputs

os.system("mkdir " + fil + "out")
os.system("mkdir " + fil + "out/step1")
#runs a check sex on data, sends output to step1/step1
os.system("plink --bfile " + fil + " --check-sex -out " + fil + "out/step1/step1")
#finds 'PROBLEM' in output
#this is where the check sex found an issue
os.system("grep 'PROBLEM' " + fil + "out/step1/step1.sexcheck > " + fil + "out/step1/issues.txt")

#open issues
f = open(fil + "out/step1/issues.txt", 'r')
s = f.readlines()
f.close()

#in each line, only return the family id and sample id
exclude = []
for each in s:
	this = each.split()
	exclude.append(this[0]+'\t'+this[1])
	
	
#write to testdata/exclude.txt, to be used for down pipe commands	
o = open(fil + "out/step1/exclude.txt", 'w')
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

os.system("mkdir " + fil + "out/step2")
os.system("mkdir " + fil + "out/step2/step2_1")
os.system("plink --bfile " + fil + " --exclude " + fil + "out/step1/exclude.txt --missing --out " + fil + "out/step2/step2_1/step2_1")

#recalculates call rate after removing SNPs with call rates <99% and creates a new set of files
#excudes data from the sex_check
#writes data to step2/step2_0/step2_0

os.system("mkdir " + fil + "out/step2/step2_0")
os.system("plink --bfile " + fil + " --exclude " + fil + "out/step1/exclude.txt --geno 0.01 --make-bed --out " + fil + " out/step2/step2_0/step2_0")

##Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#writes data to step2/step2_2/step2_2

os.system("mkdir " + fil + "out/step2/step2_2")
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --missing --out " + fil + "out/step2/step2_2/step2_2")

"""
### STEP 2 -PLOTTING###
x = fil + "out/step2/step2_2/step2_2" #insert file name here
ftype = ".imiss" #insert file type here

data = pd.read_table(x + ftype, sep= r'\s*') #use panda to read in the data from specified file

plt.figure() #create a new figure
plt.hist(data["F_MISS"], bins = 100) #add a histogram to the figure
plt.xlabel("F_MISS") #add the x label
plt.ylabel("Frequency") #add the y label
plt.title("F_MISS Frequncy Histogram") #add the title
plt.savefig(x + '_histogram.png') #save the file to specified file name as a .png
"""
### STEP 3 - Person Call Rate ###

#make directory for person call rate check output
os.system("mkdir " + fil + "out/step3")
#person call rate with standard 0.1 threshold
#write output to step5/step5
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --mind 0.1 --make-bed --out " + fil + " out/step3/step3")

### STEP 4 - Hardy Weinberg ###

#make directory for hardy-weinberg output
os.system("mkdir " + fil + "out/step4")

#write hardy-weinberg test to step4
#where SNPs with p < 1e-6 are excluded
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --hwe 1e-6 --make-bed -out " + fil + " out/step4/step4")

### STEP 5 - LD prune for relationship check & heterozygosity calculation ###
#Step 5: LD pruning
"""
os.system("mkidr " + fil + "out/step5")
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --indep-pairwise 50 5 0.3 --out " + fil + "out/step5/step5_0")


#bfile:change to .bed file from previous steps 3 and 4  

#indep-pairwise:window size in SNPs, the number of SNPs to to shift the window at each step, VIF threshold (could be 0.2 or 0.3)

#--outfile is same file as bfile for simplicity, or new name for testing purposes

#output is 2 files of pruned SNPs: .prune.in and .prune.out 



#heterzygosity calculation





#Step 6: Relationship and IBD check

 

#Plot IBD here

#determine min relatedness value to be used



min_relatedness = 0

#filter related 

os.system("plink --bfile" + bfile + " --extract " + ofile + ".prune.in --genome --min " + min_relatedness + " --out " + ofile)

#bfile: files from previous steps 3, 4, 5

#extract LD prune.in file

#min: exclude pairs that share more than 25% of genome, PI HAT pairs greater than 0.25 if highly related (relatedness of full siblings and more related), if not want to use value of 0.05 

#out: extracts SNPs to .genome out file

#output: .genome file





#write code to check for duplicates and hapmap relationships, extract hapmap exclusions from plot from ofile and make exclusion list 





#rerun relationship check with duplicates excluded

os.system("plink --bfile" + bfile + " --extract " + ofile + ".prune.in --remove exclusionlist.txt --genome --min " + min_relatedness + " --out ...duplicates")



#if any phi-hat values are above the min_relatedness value in .genome file remove them

#write code to create txt file of those

#os.system("plink --bfile" + bfile + " --extract " + ofile + ".prune.in --remove extractedfilesremoved.txt --genome --out ...extractedfilesremovedagain")





#Step 7: Heterozygosity check 



#Plot here





#filter any outliers from plot, mean sd +/-3

os.system("plink --bfile" + bfile + " --het --extract " + ofile + ".prune.in --remove extractedfilesremoved.txt --out ...extractedfilesremovedagain")



#calculates inbreeding coeffecients 



chr = 0

#Step 8:PCA prep and pca

os.system("plink --bfile pop_HM3_hg19_forPCA --chr " + chr + " --make-bed --out ...chr")

os.system("cut -f 2 ...chr > chrlist")



os.system("plink --bfile " + bfile + " --remove ...hetoutlierlist.txt --exclude chrlist --make-bed --out pop_HM3_hg19_forPCA")

os.system("module load eigensoft/5.0.1 ")



bed = ""

bim = ""

fam = ""



os.system("plink --bfile pop_HM3_hg19_forPCA --bmerge " + bed + " " + bim + " " + fam + " --make-bed --out ...")

#merge qc files with HAPMAP files

#use bfile from previous step, --bmerge bim, fam, bed files from wheelerlab2 folders

##then --make-bed, --idepen-pairwise and --recode, if necessary awk, then make par, then smartpca -p file.par
### STEP 6 - Relationship check ###

### STEP 7 - Heterozygosity check ###
"""
