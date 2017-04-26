#wrapper code

import os                           #imports os module to allow the code to use the command line
import argparse                     #imports the argparse module which accepts input from the command line to use in the running of the code
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import sys


def plot(out, name, type, var):
	data = pd.read_table(name + type, sep= r'\s*', engine = "python") #use panda to read in the data from specified file
	
	plt.figure()
	plt.hist(data[var], bins = 100) #add a histogram to the figure
	plt.xlabel(str(var)) #add the x label
	plt.ylabel("Frequency") #add the y label
	plt.title(str(var) + " Frequncy Histogram") #add the title
	plt.savefig(str(out) + ".png") #save the file to specified file name as a .png

	
def IBDplot(out, name):
	data = pd.read_table(name, sep = r'\s*', engine = "python")

	plt.figure()
	plt.scatter(data["Z0"], data["Z1"])
	plt.xlabel("Z0")
	plt.ylabel("Z1")
	plt.title("Check Identity by Descent (IBD)")
	plt.savefig(str(out) + ".png") #save the file to specified file name as a .png

	
def HETplot(out, name, var):
	data = pd.read_table(name, sep= r'\s*', engine = "python") #use panda to read in the data from specified file
	
	sdn = 6 #This tells you how many SDs to plot the line away from change to personal preference
	
	plt.figure()
	plt.hist(data[var], bins = 100) #add a histogram to the figure
	plt.xlabel(str(var)) #add the x label
	plt.ylabel("Frequency") #add the y label
	plt.title(str(var) + " Frequncy Histogram") #add the title
	
	mean = data["F_MISS"].mean()
	std = data["F_MISS"].std()
	
	plt.axvline(x = mean + std * sdn, color = 'r')
	plt.axvline(x = mean - std * sdn, color = 'r')
	
	plt.savefig(str(out)) #save the file to specified file name as a .png
		
	
### Step1: Sex Check ###
def step1(fil):
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

	
### Step2: SNP call rate ###
def step2(fil):
	#SNP call rate
	#thresholds set to 0.01
	#Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
	#excludes data from the sex_check
	#writes data to step2/step2_1/step2_1

	os.system("mkdir " + fil + "out/histograms")
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
	
	plot(fil + "out/histograms/step2_1-imiss", fil + "out/step2/step2_1/step2_1", ".imiss", "F_MISS")
	plot(fil + "out/histograms/step2_2-imiss", fil + "out/step2/step2_2/step2_2", ".imiss", "F_MISS")
	plot(fil + "out/histograms/step2_2-lmiss", fil + "out/step2/step2_2/step2_2", ".lmiss", "F_MISS")
	

	
### Step3: Person Call Rate ###
def step3(fil):
	#make directory for person call rate check output
	os.system("mkdir " + fil + "out/step3")
	os.system("mkdir " + fil + "out/step3/step3_0")
	os.system("mkdir " + fil + "out/step3/step3_1")
	os.system("mkdir " + fil + "out/step3/step3_2")	
	os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --missing --out " + fil + "out/step3/step3_1/step3_1")
	#person call rate with standard 0.1 threshold
	#write output to step3/step3
	os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --mind 0.1 --make-bed --out " + fil + "out/step3/step3_0/step3_0")
	os.system("plink --bfile " + fil + "out/step3/step3_0/step3_0 --missing --out " + fil + "out/step3/step3_2/step3_2")
	
	plot(fil + "out/histograms/step3_1-imiss", fil + "out/step3/step3_1/step3_1", ".imiss", "F_MISS")	
	plot(fil + "out/histograms/step3_2-imiss", fil + "out/step3/step3_2/step3_2", ".imiss", "F_MISS")
	plot(fil + "out/histograms/step3_2-lmiss", fil + "out/step3/step3_2/step3_2", ".lmiss", "F_MISS")

	
### Step4: Hardy-Weinberg ###
def step4(fil):
	#make directory for hardy-weinberg output
	os.system("mkdir " + fil + "out/step4")
	os.system("mkdir " + fil + "out/step4/step4_0")
	os.system("mkdir " + fil + "out/step4/step4_1")

	#write hardy-weinberg test to step4
	#where SNPs with p < 1e-6 are excluded
	os.system("plink --bfile " + fil + "out/step3/step3_0/step3_0 --hwe 1e-6 --make-bed --out " + fil + "out/step4/step4_0/step4_0")
	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --hardy --out " + fil + "out/step4/step4_1/step4_1")
	
	plot(fil + "out/histograms/step4_1-hwe", fil + "out/step4/step4_1/step4_1", ".hwe", "P")
	

### Step5: LD pruning ###
def step5(fil):
	os.system("mkdir " + fil + "out/step5")
	os.system("mkdir " + fil + "out/step5/step5_1")

	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --indep-pairwise 50 5 0.3 --out " + fil + "out/step5/step5_1/step5_1")
	#indep-pairwise:window size in SNPs, the number of SNPs to to shift the window at each step, VIF threshold (could be 0.2 or 0.3)
	#output is 2 files of pruned SNPs: .prune.in and .prune.out 

	
### Step6: Relationship and IBD check ###	
def step6(fil):
	os.system("mkdir " + fil + "out/step6")
	os.system("mkdir " + fil + "out/step6/step6_1") 
	os.system("mkdir " + fil + "out/step6/step6_2")
	#Plot IBD here
	
	
	#determine min relatedness value to be used from plot

	min_relatedness = raw_input("Enter value of minimum relatedness: \n Identical-twins\t 1\n Parent-child\t\t 0.5\n Full siblings\t\t 0.5\n Half-siblings\t\t 0.25\n Grandparent-grandchild\t 0.25\n Avuncular\t\t 0.25\n Half avuncular\t\t 0.125\n First-cousin\t\t 0.25\n Half-first-cousin\t 0.0625\n Half-sibling-plus-first-cousin\t 0.375\n")

	#filter related 
	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --genome --min " + str(min_relatedness) + " --out " + fil + "out/step6/step6_1/step6_1")
	
	#min: exclude pairs that share more than 25% of genome, PI HAT pairs greater than 0.25 if highly related (relatedness of full siblings and more related), if not want to use value of 0.05 
	#out: extracts SNPs to .genome out file
	#output: .genome file
	#create a list of individuals to remove due to relatedness

	#reads genome file
	f = open(fil + "out/step6/step6_1/step6_1.genome", 'r')
	r = f.readlines()
	f.close()

	#creates a list of individuals to remove due to relatedness
	#in each line, return the family id, sample id, and pi-hat value
	related = []
	for each in r:
		value = each.split()
		if value[0].isdigit() == True and float(value[9]) >= float(min_relatedness):
			related.append(value[0]+'\t'+value[1]+'\t'+value[9])
		else:
			continue

	#if the the pi-hat value is above the related threshold write values to relatedtoremove.txt	
	w = open(fil + "out/step6/step6_1/relatedtoremove.txt", 'w')
	for each in related:
		w.write(each)
		w.write('\n')
	w.close()
	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_1/step5_1.prune.in --remove " + fil + "out/step6/step6_1/relatedtoremove.txt --make-bed --out  " + fil + "out/step6/step6_2/step6_2")

	#makes new bed, bim, fam files from extracted files above the relatedness threshold
	
	IBDplot(fil + "out/histograms/step6_1-LBD", fil + "out/step6/step6_1/step6_1.genome")
	
	
### Step7: heterozygosity check ###
def step7(fil):
	os.system("mkdir " + fil + "out/step7")
	os.system("mkdir " + fil + "out/step7/step7_1")
	os.system("mkdir " + fil + "out/step7/step7_2")

	#Heterzygosity check of file after extracting individuals with relatedness above the theshold 
	os.system("plink --bfile " + fil + "out/step6/step6_2/step6_2 --het --out " + fil + "out/step7/step7_1/step7_1")
	#output .het file of inbreeding coefficients for plotting and .hh file

	#Plot Het here
	HETplot(fil + "out/histograms/step7_1-het.png", fil + "out/step7/step7_1/step7_1.het", "F")

	#filter any outliers from plot, mean sd +/-3
	os.system("plink --bfile " + fil + "out/step6/step6_2/step6_2 --remove " + fil + "out/step7/step7_1/step7_1 --make-bed --out " + fil + "out/step7/step7_2/step7_2")
	#calculates inbreeding coeffecients
	

def step8(fil):
	os.system("mkdir " + fil + "out/step8")
	os.system("mkdir " + fil + "out/step8/step8_1")
	os.system("mkdir " + fil + "out/step8/step8_2")
	os.system("mkdir " + fil + "out/step8/step8_3")
	os.system("mkdir " + fil + "out/step8/step8_4")

	#step 8a:
	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --bmerge /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bed /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bim /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.fam --make-bed --out " + fil + "out/step8/step8_1/step8_1")
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
	
	o = open(str(fil) + "out/step8/step8_4/step8_4.par", 'w')
	o.write("genotypename: " + str(fil) + "out/step8/step8_4/step8_4.ped\n")
	o.write("snpname: " + str(fil) + "out/step8/step8_4/step8_4.map\n")
	o.write("indivname: " + str(fil) + "out/step8/step8_4/step8_4.fam\n")
	o.write("evecoutname: " + str(fil) + "out/step8/step8_4/step8_4.evec\n")
	o.write("evaloutname: " +  str(fil) + "out/step8/step8_4/step8_4.eval\n")
	o.write("outliername: " +  str(fil) + "out/step8/step8_4/step8_4.outlier\n")
	o.write("numoutevec: 10\n")
	o.write("numoutlieriter: 0\n")
	o.write("numoutlierevec: 2\n")
	o.write("outliersigmathresh: 6\n")
	o.close()

	#os.system("module load eigensoft/5.0.1")

	#step 8h:
	os.system("smartpca -p " + fil + "out/step8/step8_4/step8_4.par")

	
	
parser = argparse.ArgumentParser()  #creates the parser list for argparse
parser.add_argument('fil', help="enter file name ex. '/home/user/desktop/infile' without extentions")
#parser.add_argument("test", help="simply a test") #testing argument
args = parser.parse_args()          #creates the list of aruments called args

fil = args.fil


step1(fil)
step2(fil)
step3(fil)
step4(fil)
step5(fil)
step6(fil)
step7(fil)
#step8(fil)