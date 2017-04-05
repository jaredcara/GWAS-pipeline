"""
PCA
"""
import os

#step 6a:
os.system("plink --bfile " + bfile + " --bmerge /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bed /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.bim /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig.fam --make-bed --out ...step6a")
#merge QC bfile from previous step 5f with hg19 bed, bim, fam files
#makes -merge.missnp file
  
#step 6b:
os.system("plink --bfile /home/wheelerlab2/Data/HAPMAP3_hg19/HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig --exclude ...step6a-merge.missnp --make-bed --out ...step6b")
#merge again excluding missing SNPs
#out makes bed, bim, fam files

#step 6c:
os.system("plink --bfile " + bfile + " --bmerge step6b.bed step6b.bim step6b.fam --make-bed --out ...step6c")
#merge again
#out makes bed, bim, fam files 

#step 6d:
os.system("plink --bfile ...step6c --geno 0.2 --maf 0.05 --make-bed --out ...step6d")
#keeps SNPs of merged file to genotypes above 90%
#out bed, bim, fam files

#step 6e:
os.system("plink --bfile ...step6d --indep-pairwise 50 5 0.3 --recode --out ...step6e")
#makes .map and .ped files for smartpca 
#makes ..step6e.prune.in and prune.out files 

#step 6f:
os.system("awk '{print $1,$2,$3,$4,$5,1}' ...step6d.fam > ...step6e.fam")
#extracts columns from 6d fam file to 6e

#step 6g:
b = sys.argv[0]
num = sys.argv[1]

print "genotypename: "+ b + ".ped\n";
print "snpname: " + b + ".map\n";
print "indivname: " + b + ".fam\n";
print "evecoutname: " + b + ".evec\n";
print "evaloutname: " + b + ".eval\n";
print "outliername: " + b + ".outlier\n";
print "numoutevec: 10\n";
print "numoutlieriter: " + num + "\n";
print "numoutlierevec: 2\n";
print "outliersigmathresh: 6\n";
#create parfile for smartpca

os.system("module load eigensoft/5.0.1")

#step 6h:
os.system("smartpca -p ...step6f.par")

