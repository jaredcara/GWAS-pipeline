
import os

bfile = ""
#from previous steps of QC
ofile = ""
#out file

#Step 5: LD pruning
os.system("plink --bfile" + bfile + " --indep-pairwise 50 5 0.3 --out " + ofile)
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