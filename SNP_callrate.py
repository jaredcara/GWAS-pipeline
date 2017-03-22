import os

#SNP call rate
#thresholds set to 0.01

#Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#excludes data from the sex_check
#writes data to step2/step2

os.system("mkdir /home/jcara/step2")
os.system("plink --bfile /home/jcara/testdata/testdata --exclude /home/jcara/testdata/exclude.txt --missing --out /home/jcara/step2/step2")

#recalculates call rate after removing SNPs with call rates <99% and creates a new set of files
#excudes data from the sex_check
#writes data to step3/step3

os.system("mkdir /home/jcara/step3")
os.system("plink --bfile /home/jcara/testdata/testdata --exclude /home/jcara/testdata/exclude.txt --geno 0.01 --make-bed --out /home/jcara/step3/step3")

##Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#writes data to step4/step4

os.system("mkdir /home/jcara/step4")
os.system("plink --bfile /home/jcara/step3/step3 --missing --out /home/jcara/step4/step4")

