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
os.system("plink --bfile " + fil + " --exclude " + fil + "out/step1/exclude.txt --geno 0.01 --make-bed --out " + fil + "out/step2/step2_0/step2_0")

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
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --mind 0.1 --make-bed --out " + fil + "out/step3/step3")

### STEP 4 - Hardy Weinberg ###

#make directory for hardy-weinberg output
os.system("mkdir " + fil + "out/step4")
os.system("mkdir " + fil + "out/step4/step4_0")
os.system("mkdir " + fil + "out/step4/step4_1")

#write hardy-weinberg test to step4
#where SNPs with p < 1e-6 are excluded
os.system("plink --bfile " + fil + "out/step3/step3 --hwe 1e-6 --make-bed --out " + fil + "out/step4/step4_0/step4_0")
os.system("plink --bfile " + fil + "out/step4/step4 --hardy --out " + fil + "out/step4/step4_1/step4_1")

### STEP 5 - LD prune for relationship check & heterozygosity calculation ###
#Step 5: LD pruning

os.system("mkdir " + fil + "out/step5")
os.system("mkdir " + fil + "out/step5/step5_1")

os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --indep-pairwise 50 5 0.3 --out " + fil + "out/step5/step5_1/step5_1")
#indep-pairwise:window size in SNPs, the number of SNPs to to shift the window at each step, VIF threshold (could be 0.2 or 0.3)
#output is 2 files of pruned SNPs: .prune.in and .prune.out 



#heterzygosity calculation



#Step 6: Relationship and IBD check
os.system("mkdir " + fil + "out/step6")
os.system("mkdir " + fil + "out/step6/step6_1") 


#Plot IBD here



#determine min relatedness value to be used from plot


min_relatedness = raw_input("Enter value of minimum relatedness: \n Identical-twins\t 1\n Parent-child\t\t 0.5\n Full siblings\t\t 0.5\n Half-siblings\t\t 0.25\n Grandparent-grandchild\t 0.25\n Avuncular\t\t 0.25\n Half avuncular\t\t 0.125\n First-cousin\t\t 0.25\n Half-first-cousin\t 0.0625\n Half-sibling-plus-first-cousin\t 0.375\n")
#prompts user for min relatedness value

#filter related 
os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --genome --min " + min_relatedness + " --out " + fil + "out/step6/step6_1/step6_1")
#extract LD prune.in file
#min: exclude pairs that share more than 25% of genome, PI HAT pairs greater than 0.25 if highly related (relatedness of full siblings and more related), if not want to use value of 0.05 
#out: extracts SNPs to .genome out file
#output: .genome file

#reads genome file
f = open(fil + "out/step6/step6_1/step6_1.genome", 'r')
r = f.readlines()
f.close()

#creates a list of individuals to remove due to relatedness
#in each line, return the family id, sample id, and pi-hat value
relatedness = 0.1875
related = []
for each in r:
    value = each.split()
    if value[0].isdigit() == True and float(value[9]) >= relatedness:
        related.append(value[0]+'\t'+value[1]+'\t'+value[9])
    else:
        continue
	
#if the the pi-hat value is above the related threshold write values to relatedtoremove.txt	
w = open(fil + "out/step6/step6_1/relatedtoremove.txt", 'w')
for each in related:
	each.write(i)
	each.write('\n')
w.close()

#Step 7: Heterozygosity check
os.system("mkdir " + fil + "out/step7")
os.system("mkdir " + fil + "out/step7/step7_1")
os.system("mkdir " + fil + "out/step7/step7_2")
os.system("mkdir " + fil + "out/step7/step7_3")
os.system("mkdir " + fil + "out/step7/step7_4")
os.system("mkdir " + fil + "out/step7/step7_5")
os.system("mkdir " + fil + "out/step7/step7_6")

os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --het --out " + fil + "out/step7/step7_1/step7_1")
#output .het file of inbreeding coefficients for plotting and .hh file



#write code to check for duplicates and hapmap relationships, extract hapmap exclusions from plot from ofile and make exclusion list 




#rerun relationship check with duplicates excluded
#os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --remove exclusionlist.txt --genome --min " + min_relatedness + " --out " + fil + "out/step7/step7_2/step7_2")


#os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --remove extractedfilesremoved.txt --genome --out " + fil + "out/step7/step7_3/step7_3")

 
os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --remove " + fil + "out/step6/step6_1/relatedtoremove.txt --make-bed --out  " + fil + "out/step7/step7_4/step7_4")
#makes bed, bim, fam files from extracted files above the threshold
#removes people with min_relatedness from step7_1


os.system("plink --bfile " + fil + "out/step7/step7_4/step7_4 --het --out " + fil + "out/step7/step7_5/step7_5")
#Checks heterozygosity for individuals with <= relatedness


	  
#Plot Het here




#filter any outliers from plot, mean sd +/-3
os.system("plink --bfile " + fil + "out/step7/step7_4/step7_4 --het --extract " + fil + "out/step5/step5_1/step5_1.prune.in --remove extractedfilesremoved.txt --out ...extractedfilesremovedagain")
os.system("plink --bfile " + fil + "out/step7/step7_4/step7_4 --remove " + fil + "out/step7/step7_5/step7_5.txt --make-bed --out " + fil + "out/step7/step7_6/step7_6")
#calculates inbreeding coeffecients 


#Step 8:PCA prep and pca

os.system("mkdir " + fil + "out/step8")
os.system("mkdir " + fil + "out/step8/step8_1")
os.system("mkdir " + fil + "out/step8/step8_2")
os.system("mkdir " + fil + "out/step8/step8_3")
os.system("mkdir " + fil + "out/step8/step8_4")

#step 8a:
os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --bmerge /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bed /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bim /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.fam --make-bed --out " + fil + "out/step8/step8_1/step8_1")
#plink --bfile testdataout/step2/step2_0 --bmerge /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bed /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bim /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.fam --make-bed --out " + fil + "out/step/step8_1/step8_1
#merge QC bfile from previous step 5f with hg19 bed, bim, fam files
#makes -merge.missnp file

#step 8b:
os.system("plink --bfile /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig --exclude " + fil + "out/step8/step8_1/step8_1-merge.missnp --make-bed --out " + fil + "out/step8/step8_1/step8_1")
#merge again excluding missing SNPs
#out makes bed, bim, fam files

#step 8c:
os.system("plink --bfile " + fil + "out/step8/step8_1/step8_1 --bmerge " + fil + "out/step8/step8_1/step8_1.bed " + fil + "out/step8/step8_1/step8_1.bim " + fil + "out/step8/step8_1/step8_1.fam --make-bed --out " + fil + "out/step8/step8_2/step8_2")
#merge again
#out makes bed, bim, fam files 

#step 8d:
os.system("plink --bfile " + fil + "out/step8/step8_2/step8_2 --geno 0.2 --maf 0.05 --make-bed --out " + fil + "out/step8/step8_3/step8_3")
#keeps SNPs of merged file to genotypes above 90%
#out bed, bim, fam files

#step 8e:
os.system("plink --bfile " + fil + "out/step8/step8_3/step8_3 --indep-pairwise 50 5 0.3 --recode --out " + fil + "out/step8/step8_4/step8_4")
#makes .map and .ped files for smartpca 
#makes ..step6e.prune.in and prune.out files 

#step 8f:
os.system("awk '{print $1,$2,$3,$4,$5,1}' " + fil + "out/step8/step8_3/step8_3.fam > " + fil + "out/step8/step8_4/step8_4.fam")
#extracts columns from 6d fam file to 6e

#step 8g:
#create parfile for smartpca
os.system("python create_par_file.py " + fil + "out/step8/step8_4/step8_4 0 > " + fil + "out/step8/step8_4/step8_4.par")

#os.system("module load eigensoft/5.0.1")

#step 8h:
os.system("smartpca -p " + fil + "out/step8/step8_4/step8_4.par")

### STEP 6 - Relationship check ###

### STEP 7 - Heterozygosity check ###
