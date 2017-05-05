#wrapper code

import os                           #imports os module to allow the code to use the command line
import argparse                     #imports the argparse module which accepts input from the command line to use in the running of the code
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy


def plot(out, name, type, var):
	data = pd.read_table(fil + name + type, sep= r'\s*', engine = "python") #use panda to read in the data from specified file
	

	res.write(out)
	res.write('\n')
	res.write(str(data[var].describe()))	#prints basic statistic description of data (count, mean, std dev, quartiles)
	res.write('\n')
	res.write('\n')	


	plt.figure()
	plt.hist(data[var], bins = 100) #add a histogram to the figure
	plt.xlabel(str(var)) #add the x label
	plt.ylabel("Frequency") #add the y label
	plt.title(str(var) + " Frequncy Histogram") #add the title
	plt.savefig(fil + "out/histograms/" + str(out) + ".png", bbox_inches = 'tight', format = 'png', dpi = 900) #save the file to specified file name as a .png

	
def IBDplot(out, name):
	data = pd.read_table(fil + name, sep = r'\s*', engine = "python")

	plt.figure()
	plt.scatter(data["Z0"], data["Z1"])
	plt.xlabel("Z0")
	plt.ylabel("Z1")
	plt.title("Check Identity by Descent (IBD)")
	plt.savefig(fil + "out/histograms/" + str(out) + ".png", bbox_inches = 'tight', format = 'png', dpi = 900) #save the file to specified file name as a .png

	
def HETplot(out, name, var):
	data = pd.read_table(fil + name, sep= r'\s*', engine = "python") #use panda to read in the data from specified file

	
	res.write(out)
	res.write('\n')
	res.write(str(data[var].describe())) #prints basic statistic description of data (count, mean, std dev, quartiles)
	res.write('\n')
	res.write('\n')


	plt.figure()
	plt.hist(data[var], bins = 100) #add a histogram to the figure
	plt.xlabel(str(var)) #add the x label
	plt.ylabel("Frequency") #add the y label
	plt.title(str(var) + " Frequncy Histogram") #add the title
	
	mean = data["F"].mean()
	std = data["F"].std()
	
	plt.axvline(x = mean + std * sdn, color = 'r')
	plt.axvline(x = mean - std * sdn, color = 'r')
	
	plt.savefig(fil + "out/histograms/" + str(out), bbox_inches = 'tight', format = 'png', dpi = 900) #save the file to specified file name as a .png

	f = open(fil + name, 'r')
	s = f.readlines()
	f.close()
	
	these = []
	
	for each in s:
		this = each.split()
		if this[5] >= (mean + (std * sdn)):
			if this[5] <= (mean - (std * sdn)):
				print this[0]
				these.eppend(this[0]+'\t'+this[1])
		
	return these
		
	

	
#to be used after step8_6	
def PCAplot(name):
	r = open(fil + name + ".evec", 'r') #open the evec file
	e = r.readline() #read the first line where all the eigen values are stored
	r.close() #close the file
	e = e.split() #put everything into an array
	del e[0] #delete the first element (it is not needed for calculation)
	e = [float(x) for x in e] #convert all elements in array to float values
	e = [str(round(x/sum(e), 3)) for x in e] #perform calculations rounding to 3 digits
	res.write("PCA")
	res.write('\n')
	res.write('\t'.join(e)) #print the calculated values

	pd.options.mode.chained_assignment = None #remove warning that pops up
	hapmapinfo = pd.read_table(hap, sep = r'\s*', engine = 'python', header = None, usecols=(0,2), names = ["pop", 'IID']) #read in the location of the population data
	fam = pd.read_table(fil + name + ".fam", sep = r'\s*', engine = 'python', header = None, usecols=(0,1), names = ["FID", 'IID']) #read in the data from the fam file
	popinfo = fam.join(hapmapinfo.set_index("IID"), on = "IID") #merge the two previous files using the IID values
	evec = pd.read_table(fil + name + ".evec", sep = r'\s*', engine = 'python', header = None, skiprows = 1) #read in the evec file
	i = 0
	while i < len(evec): #fixes the evec IID columns
		x = evec[0][i].index(':')
		evec[0][i]= evec[0][i][x+1:]
		i += 1
	evec.columns = ['IID', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10', 'CONTROL'] #renames the columns
	PCA = evec.join(popinfo.set_index('IID'), on = 'IID') #merges everything by IID and the order for index is as follows (starting at index 1): IID PC1 PC2 PC3 PC4 PC5 PC6 PC7 PC8 PC9 PC10 CONTROL FID POP
	plt.figure() #creates a new figure
	for row in PCA.itertuples(): #plots the data by the family it is from
		if row[14] == "ASN": #Plots the ASN and makes their points red
			A = plt.scatter(row[2], row[3], c = 'r', alpha = .5, s = 20)
		elif row[14] == "CEU": #Plots the CEU and makes their points blue
			C = plt.scatter(row[2], row[3], c = 'b', alpha = .5, s = 20)
		elif row[14] == "YRI": #Plots the YRI and makes their points magenta
			Y = plt.scatter(row[2], row[3], c = 'm', alpha = .5, s = 20)
		else: #Plots everything else and makes the points green
			G = plt.scatter(row[2], row[3], c = 'g', alpha = .5, s = 20)
	plt.xlabel("PC1") #adds xlabel
	plt.ylabel("PC2") #adds ylabel
	plt.title("PCA Plot 1 (PC1 vs PC2)") #addes title
	plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1) #adds the legend
	plt.savefig(fil + "out/histograms/PCA1.png", bbox_inches = 'tight', format = 'png', dpi = 900) #saves the figure

	plt.figure() #this code is the same as above except with different columns used to create the graph
	for row in PCA.itertuples():
		if row[14] == "ASN":
			A = plt.scatter(row[2], row[4], c = 'r', alpha = .5, s = 20)
		elif row[14] == "CEU":
			C = plt.scatter(row[2], row[4], c = 'b', alpha = .5, s = 20)
		elif row[14] == "YRI":
			Y = plt.scatter(row[2], row[4], c = 'm', alpha = .5, s = 20)
		else:
			G = plt.scatter(row[2], row[4], c = 'g', alpha = .5, s = 20)
	plt.xlabel("PC1")
	plt.ylabel("PC3")
	plt.title("PCA Plot 2 (PC1 vs PC3)")
	plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
	plt.savefig(fil + "out/histograms/PCA2.png", bbox_inches = 'tight', format = 'png', dpi = 900) 

	plt.figure() #this code is the same as above except with different columns used to create the graph
	for row in PCA.itertuples():
		if row[14] == "ASN":
			A = plt.scatter(row[3], row[4], c = 'r', alpha = .5, s = 20)
		elif row[14] == "CEU":
			C = plt.scatter(row[3], row[4], c = 'b', alpha = .5, s = 20)
		elif row[14] == "YRI":
			Y = plt.scatter(row[3], row[4], c = 'm', alpha = .5, s = 20)
		else:
			G = plt.scatter(row[3], row[4], c = 'g', alpha = .5, s = 20)
	plt.xlabel("PC2")
	plt.ylabel("PC3")
	plt.title("PCA Plot 3 (PC2 vs PC3)")
	plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
	plt.savefig(fil + "out/histograms/PCA3.png", bbox_inches = 'tight', format = 'png', dpi = 900) 

	xvals = []
	yvals = []
	plt.figure() #this code is the similar to above except it adds lines 5 std dev away from selected point
	for row in PCA.itertuples():
		if row[14] == "ASN":
			A = plt.scatter(row[2], row[3], c = 'r', alpha = .5, s = 20)
		elif row[14] == "CEU":
			C = plt.scatter(row[2], row[3], c = 'b', alpha = .5, s = 20)
		elif row[14] == "YRI":
			Y = plt.scatter(row[2], row[3], c = 'm', alpha = .5, s = 20)
			xvals.append(row[2]) #used to add bars to PCA plot
			yvals.append(row[3]) #move these two lines under desired population for bars be sure to change the x and y for where the values are coming from
		else:
			G = plt.scatter(row[2], row[3], c = 'g', alpha = .5, s = 20)
	xmean = sum(xvals)/float(len(xvals)) #calculate the mean
	ymean = sum(yvals)/float(len(yvals)) #calculate the mean
	xstd = numpy.std(xvals) #calculate std dev
	ystd = numpy.std(yvals) #calculate std dev
	sdn = 5 #number of standard deviations away from mean you want line to be
	plt.axvline(x= xmean+xstd*sdn, color = 'k') #add line x sd away from xmean
	plt.axvline(x= xmean-xstd*sdn, color = 'k')
	plt.axhline(y= ymean+ystd*sdn, color = 'k') #add line x sd away from ymean
	plt.axhline(y= ymean-ystd*sdn, color = 'k')
	plt.xlabel("PC1")
	plt.ylabel("PC2")
	plt.title("PCA Plot 1 (PC1 vs PC2) with lines")
	plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
	plt.savefig(fil + "out/histograms/PCA1Lines.png", bbox_inches = 'tight', format = 'png', dpi = 900)
		
	
### Step1: Sex Check ###
def step1(fil):
	#make directories for step1
	os.system("mkdir " + fil + "out")
	os.system("mkdir " + fil + "out/step1")
	#runs a check sex on data, sends output to step1/step1
	os.system("plink --bfile " + fil + " --check-sex -out " + fil + "out/step1/step1")
	#check sex will output with each person who doesnot pass the QC with "PROBLEM"

	#finds 'PROBLEM' in output, where the check sex found an issue
	os.system("grep 'PROBLEM' " + fil + "out/step1/step1.sexcheck > " + fil + "out/step1/issues.txt")
	#writes all "PROBLEM"s to issues.txt
	
	#open issues, read lines
	f = open(fil + "out/step1/issues.txt", 'r')
	s = f.readlines()
	f.close()

	o = open(fil + "out/step1/exclude.txt", 'w')

	#in each line, only return the family id and sample id
	for each in s:
		this = each.split()
		o.write(this[0]+'\t'+this[1])
		o.write('\n')	
	o.close()

	
### Step2: SNP call rate ###
def step2(fil):
	#SNP call rate
	#thresholds set to 0.01
	#Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
	#excludes data from the sex_check
	#writes data to step2/step2_1/step2_1

	os.system("mkdir " + fil + "out/step2")
	os.system("mkdir " + fil + "out/step2/step2_1")
	os.system("plink --bfile " + fil + " --remove " + fil + "out/step1/exclude.txt --missing --out " + fil + "out/step2/step2_1/step2_1")
	
	#recalculates call rate after removing SNPs with call rates <99% and creates a new set of files
	#excudes data from the sex_check
	#writes data to step2/step2_0/step2_0

	os.system("mkdir " + fil + "out/step2/step2_0")
	os.system("plink --bfile " + fil + " --remove " + fil + "out/step1/exclude.txt --geno 0.01 --make-bed --out " + fil + "out/step2/step2_0/step2_0")

	##Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
	#writes data to step2/step2_2/step2_2

	os.system("mkdir " + fil + "out/step2/step2_2")
	os.system("plink --bfile " + fil + "out/step2/step2_0/step2_0 --missing --out " + fil + "out/step2/step2_2/step2_2")
	
	plot("step2_1-imiss", "out/step2/step2_1/step2_1", ".imiss", "F_MISS")
	plot("step2_2-imiss", "out/step2/step2_2/step2_2", ".imiss", "F_MISS")
	plot("step2_2-lmiss", "out/step2/step2_2/step2_2", ".lmiss", "F_MISS")
	

	
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
	
	plot("step3_1-imiss", "out/step3/step3_1/step3_1", ".imiss", "F_MISS")	
	plot("step3_2-imiss", "out/step3/step3_2/step3_2", ".imiss", "F_MISS")
	plot("step3_2-lmiss", "out/step3/step3_2/step3_2", ".lmiss", "F_MISS")

	
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
	
	plot("step4_1-hwe", "out/step4/step4_1/step4_1", ".hwe", 'P')
	

### Step5: LD pruning ###
def step5(fil):
	os.system("mkdir " + fil + "out/step5")
	os.system("mkdir " + fil + "out/step5/step5_0")
	os.system("mkdir " + fil + "out/step5/step5_1")

	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --indep-pairwise 50 5 0.3 --out " + fil + "out/step5/step5_0/step5_0")
	#indep-pairwise:window size in SNPs, the number of SNPs to to shift the window at each step, VIF threshold (could be 0.2 or 0.3)
	#output is 2 files of pruned SNPs: .prune.in and .prune.out 
	os.system("plink --bfile " + fil + "out/step4/step4_0/step4_0 --extract " + fil + "out/step5/step5_0/step5_0.prune.in --make-bed --out " + fil + "out/step5/step5_1/step5_1")
	

### Step6: Relationship and IBD check ###	
def step6(fil):
	os.system("mkdir " + fil + "out/step6")
	os.system("mkdir " + fil + "out/step6/step6_0") 
	os.system("mkdir " + fil + "out/step6/step6_1")
	
	
	#determine min relatedness value to be used from plot

	min_relatedness = ibd
	
	#filter related 
	os.system("plink --bfile " + fil + "out/step5/step5_1/step5_1 --genome --min " + str(min_relatedness) + " --out " + fil + "out/step6/step6_0/step6_0")
	
	#min: exclude pairs that share more than 25% of genome, PI HAT pairs greater than 0.25 if highly related (relatedness of full siblings and more related), if not want to use value of 0.05 
	#out: extracts SNPs to .genome out file
	#output: .genome file
	#create a list of individuals to remove due to relatedness

	#reads genome file
	f = open(fil + "out/step6/step6_0/step6_0.genome", 'r')
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
	w = open(fil + "out/step6/step6_0/relatedtoremove.txt", 'w')
	for each in related:
		w.write(each)
		w.write('\n')
	w.close()
	os.system("plink --bfile " + fil + "out/step5/step5_1/step5_1 --remove " + fil + "out/step6/step6_0/relatedtoremove.txt --make-bed --out  " + fil + "out/step6/step6_1/step6_1")

	#makes new bed, bim, fam files from extracted files above the relatedness threshold
	
	IBDplot("step6_0-IBD", "out/step6/step6_0/step6_0.genome")
	
	
### Step7: heterozygosity check ###
def step7(fil):
	os.system("mkdir " + fil + "out/step7")
	os.system("mkdir " + fil + "out/step7/step7_0")
	os.system("mkdir " + fil + "out/step7/step7_1")

	#Heterzygosity check of file after extracting individuals with relatedness above the theshold 
	os.system("plink --bfile " + fil + "out/step6/step6_1/step6_1 --het --out " + fil + "out/step7/step7_0/step7_0")
	#output .het file of inbreeding coefficients for plotting and .hh file

	#Plot Het here
	these = HETplot("step7_0-het.png", "out/step7/step7_0/step7_0.het", "F")

	o = open(fil + "out/step7/step7_0/issues.txt", 'w')
	for each in these:
		o.write(each)
		o.write('\n')
	
	o.close()
	
	
	#filter any outliers from plot, mean sd +/-3
	os.system("plink --bfile " + fil + "out/step6/step6_1/step6_1 --remove " + fil + "out/step7/step7_0/issues.txt --make-bed --out " + fil + "out/step7/step7_1/step7_1")
	#calculates inbreeding coeffecients
	
### Step 8: PCA ###
def step8(fil):
	os.system("mkdir " + fil + "out/step8")
	os.system("mkdir " + fil + "out/step8/step8_0")
	os.system("mkdir " + fil + "out/step8/step8_1")
	os.system("mkdir " + fil + "out/step8/step8_2")
	os.system("mkdir " + fil + "out/step8/step8_3")
	os.system("mkdir " + fil + "out/step8/step8_4")
	os.system("mkdir " + fil + "out/step8/step8_5")

	
	os.system("plink --bfile " + fil + "out/step7/step7_1/step7_1 --bmerge " + merge + ".bed " + merge + ".bim " + merge + ".fam --make-bed --out " + fil + "out/step8/step8_0/step8_0")
	#merge QC bfile from previous step 5f with hg19 bed, bim, fam files
	#makes -merge.missnp file

	
	os.system("plink --bfile " + merge + " --exclude " + fil + "out/step8/step8_0/step8_0-merge.missnp --geno 0.1 --make-bed --out " + fil + "out/step8/step8_1/step8_1_HAPMAP")
	#merge again excluding missing SNPs
	#out makes bed, bim, fam files

	
	os.system("plink --bfile " + fil + "out/step7/step7_1/step7_1 --bmerge " + fil + "out/step8/step8_1/step8_1_HAPMAP.bed " + fil + "out/step8/step8_1/step8_1_HAPMAP.bim " + fil + "out/step8/step8_1/step8_1_HAPMAP.fam --geno 0.1 --make-bed --out " + fil + "out/step8/step8_2/step8_2")
	#merge again
	#out makes bed, bim, fam files 

	
	#grep Warning snps 
	os.system("grep 'Warning: Variants' " + fil + "out/step8/step8_2/step8_2.log > " + fil + "out/step8/step8_2/duplicateSNPs.txt")
	#merge again
	#only save input in quotes, then remove them
	f = open(fil + "out/step8/step8_2/duplicateSNPs.txt", 'r')
	r = f.readlines()
	f.close()
	
	
	#in each line only return the duplicate SNP name`
	#remove both or just one?
	duplicates = []
	for each in r:
		each = each.replace("'", "")
		snp = each.split()
		duplicates.append(snp[2]+'\t'+snp[4])
	
	
	#write to testdata/exclude.txt, to be used for down pipe commands    
	w = open(fil + "out/step8/step8_2/duplicateSNPs.txt", 'w')
	for each in duplicates:
		w.write(each)
		w.write('\n')
	w.close()
	
	os.system("plink --bfile " + fil + "out/step7/step7_1/step7_1 --bmerge " + fil + "out/step8/step8_1/step8_1_HAPMAP.bed " + fil + "out/step8/step8_1/step8_1_HAPMAP.bim " + fil + "out/step8/step8_1/step8_1_HAPMAP.fam --exclude " + fil + "out/step8/step8_2/duplicateSNPs.txt --geno 0.1 --make-bed --out " + fil + "out/step8/step8_3/step8_3")
 	#merge again without duplicates
 
    	os.system("plink --bfile " + fil + "out/step8/step8_3/step8_3 --geno 0.1 --maf 0.05 --make-bed --out " + fil + "out/step8/step8_4/step8_4")
    	#keeps SNPs of merged file to genotypes above 90%
    	#out bed, bim, fam files
    
    	os.system("plink --bfile " + fil + "out/step8/step8_3/step8_3 --indep-pairwise 50 5 0.3 --recode --out " + fil + "out/step8/step8_4/step8_4")
    	#makes .map and .ped files for smartpca
    	#makes ..step8e.prune.in and prune.out files 

    	os.system("awk '{print $1,$2,$3,$4,$5,1}' " + fil + "out/step8/step8_3/step8_3.fam > " + fil + "out/step8/step8_4/step8_4.fam")
   	#extracts columns from 6d fam file to 6e

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


   	os.system("smartpca -p " + fil + "out/step8/step8_4/step8_4.par")
    
    	PCAplot("out/step8/step8_4/step8_4")
	
	###Use code below instead if merge is unsuccessful### 
	'''
	#Remove duplicates from filtered HAPMAP file
	os.system("plink --bfile " + fil + "out/step8/step8_1/step8_1_HAPMAP --remove " + fil + "out/step8/step8_2/duplicateSNPs.txt --geno 0.1 --make-bed --out " + fil + "out/step8/step8_3/step8_3_HAPMAP")
	
	#Remove duplicates from QC file
	os.system("plink --bfile " + fil + "out/step8/step8_2/step8_2 --remove " + fil + "out/step8/step8_2/duplicateSNPs.txt --geno 0.1 --make-bed --out " + fil + "out/step8/step8_3/step8_3")
	
	#merge again without duplicates
	os.system("plink --bfile " + fil + "out/step8/step8_3/step8_3 --geno 0.1 --exclude " + fil + "out/step8/step8_2/duplicateSNPs.txt --bmerge " + fil + "out/step8/step8_3/step8_3_HAPMAP.bed " + fil + "out/step8/step8_3/step8_3_HAPMAP.bim " + fil + "out/step8/step8_3/step8_3_HAPMAP.fam --make-bed --out " + fil + "out/step8/step8_4/step8_4")

	os.system("plink --bfile " + fil + "out/step8/step8_4/step8_4 --geno 0.1 --maf 0.05 --make-bed --out " + fil + "out/step8/step8_5/step8_5")
	#keeps SNPs of merged file to genotypes above 90%
	#out bed, bim, fam files
	
	os.system("plink --bfile " + fil + "out/step8/step8_4/step8_4 --indep-pairwise 50 5 0.3 --recode --out " + fil + "out/step8/step8_5/step8_5")
	#makes .map and .ped files for smartpca
	#makes ..step8e.prune.in and prune.out files 

	os.system("awk '{print $1,$2,$3,$4,$5,1}' " + fil + "out/step8/step8_4/step8_4.fam > " + fil + "out/step8/step8_5/step8_5.fam")
	#extracts columns from 6d fam file to 6e

	#create parfile for smartpca

	o = open(str(fil) + "out/step8/step8_5/step8_5.par", 'w')
	o.write("genotypename: " + str(fil) + "out/step8/step8_5/step8_5.ped\n")
	o.write("snpname: " + str(fil) + "out/step8/step8_5/step8_5.map\n")
	o.write("indivname: " + str(fil) + "out/step8/step8_5/step8_5.fam\n")
	o.write("evecoutname: " + str(fil) + "out/step8/step8_5/step8_5.evec\n")
	o.write("evaloutname: " +  str(fil) + "out/step8/step8_5/step8_5.eval\n")
	o.write("outliername: " +  str(fil) + "out/step8/step8_5/step8_5.outlier\n")
	o.write("numoutevec: 10\n")
	o.write("numoutlieriter: 0\n")
	o.write("numoutlierevec: 2\n")
	o.write("outliersigmathresh: 6\n")
	o.close()


	os.system("smartpca -p " + fil + "out/step8/step8_5/step8_5.par")
	
	PCAplot("out/step8/step8_5/step8_5") '''
	### ###
	
	
### Step 9: Rerun PCA without MAPMAP ###
def step9(fil):
	os.system("mkdir " + fil + "out/step9")
	os.system("mkdir " + fil + "out/step9/9_0")
	os.system("mkdir " + fil + "out/step9/9_1")
	
	os.system("plink --bfile " + fil + "out/step7/step7_1/step7_1 --geno 0.1 --maf 0.05 --make-bed --out " + fil + "out/step9/step9_0/step9_0")
	#keeps SNPs of merged file to genotypes above 90%
	#out bed, bim, fam files
	
	os.system("plink --bfile " + fil + "out/step8/step9_0/step9_0 --indep-pairwise 50 5 0.3 --recode --out " + fil + "out/step9/step9_1/step9_1")
	#makes .map and .ped files for smartpca
	#makes ..step8e.prune.in and prune.out files 

	os.system("awk '{print $1,$2,$3,$4,$5,1}' " + fil + "out/step9/step9_0/step9_0.fam > " + fil + "out/step9/step9_1/step9_1.fam")
	#extracts columns from fam file 

	#create parfile for smartpca

	o = open(str(fil) + "out/step9/step9_1/step9_1.par", 'w')
	o.write("genotypename: " + str(fil) + "out/step9/step9_1/step9_1.ped\n")
	o.write("snpname: " + str(fil) + "out/step9/step9_1/step9_1.map\n")
	o.write("indivname: " + str(fil) + "out/ste9/step9_1/step9_1.fam\n")
	o.write("evecoutname: " + str(fil) + "out/step9/step9_1/step9_1.evec\n")
	o.write("evaloutname: " +  str(fil) + "out/step9/step9_1/step9_1.eval\n")
	o.write("outliername: " +  str(fil) + "out/step9/step9_1/step9_1.outlier\n")
	o.write("numoutevec: 10\n")
	o.write("numoutlieriter: 0\n")
	o.write("numoutlierevec: 2\n")
	o.write("outliersigmathresh: 6\n")
	o.close()


	os.system("smartpca -p " + fil + "out/step9/step9_1/step9_1.par")
	
	PCAplot("out/step9/step9_1/step9_1")

def step10(fil):
	os.system("mkdir " + fil + "out/step10")
	os.system("plink --bfile " + fil + "out/step8/step8_5/step8_5 --freq --out " + fil + "out/step10/step10")
	
	#os.system("perl HRC-1000G-check-bim.pl -b " + fil + "out/step8/step8_5/step8_5.bim -f " + fil + "out/step9/step9.frq -r " + ref + " -h")
	

	
	
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)  #creates the parser list for argparse
parser.add_argument('fil', help="Enter file name for QC, without extentions")
parser.add_argument('hap', help="Enter file name for hapmapdata, with extentions")
parser.add_argument('merge', help="Enter file name for bmerg for PCA QC, without extentions")
parser.add_argument('ibd', action = 'store', nargs = '?', type = float, default = 0.125, help = "Enter value of minimum relatedness for IBD check")
parser.add_argument('sdn', action = 'store', nargs = '?',type = int, default = 6, help = "Enter the cut off of standard deviations for heterozygosity check") #testing argument
args = parser.parse_args()          #creates the list of aruments called args

fil = args.fil
hap = args.hap
merge = args.merge
ibd = args.ibd
sdn = args.sdn



step1(fil)
os.system("mkdir " + fil + "out/histograms")
res = open(fil + "out/histograms/statistics.txt", 'w')
step2(fil)
step3(fil)
step4(fil)
step5(fil)
step6(fil)
step7(fil)
step8(fil)
step9(fil)
step10(fil)
res.close()
