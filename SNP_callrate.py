import os

#SNP call rate
#thresholds set to 0.01

#Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#excludes data from the sex_check
#writes data to step2/step2_1/step2_1

os.system("mkdir /home/jcara/testing/out/step2")
os.system("mkdir /home/jcara/testing/out/step2/step2_1")
os.system("plink --bfile /home/jcara/testing/testdata/testdata --exclude /home/jcara/testing/testdata/exclude.txt --missing --out /home/jcara/testing/out/step2/step2_1/step2_1")

#recalculates call rate after removing SNPs with call rates <99% and creates a new set of files
#excudes data from the sex_check
#writes data to step2/step2_0/step2_0

os.system("mkdir /home/jcara/testing/out/step2/step2_0")
os.system("plink --bfile /home/jcara/testing//testdata/testdata --exclude /home/jcara/testing/testdata/exclude.txt --geno 0.01 --make-bed --out /home/jcara/testing/out/step2/step2_0/step2_0")

##Creates two files: .imiss (individual) and .lmiss (SNP/locus) that details missingness in data
#writes data to step2/step2_2/step2_2

os.system("mkdir /home/jcara/testing/out/step2/step2_2")
os.system("plink --bfile /home/jcara/testing/out/step2/step2_0/step2_0 --missing --out /home/jcara/testing/out/step2/step2_2/step2_2")

